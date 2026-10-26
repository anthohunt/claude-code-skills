#!/usr/bin/env python3
"""Bounded metadata-only inventory. Writes only the explicitly requested JSON report."""
import argparse
import collections
import heapq
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def native_path(path):
    value = str(path)
    if os.name != 'nt' or value.startswith('\\\\?\\'):
        return value
    return '\\\\?\\UNC\\' + value[2:] if value.startswith('\\\\') else '\\\\?\\' + value


def storage_size(path, info):
    if hasattr(info, 'st_blocks'):
        return info.st_blocks * 512, 'st_blocks'
    if os.name == 'nt':
        import ctypes
        high = ctypes.c_uint32()
        ctypes.set_last_error(0)
        low = compressed_size(native_path(path), ctypes.byref(high))
        if low != 0xFFFFFFFF or ctypes.get_last_error() == 0:
            return (high.value << 32) | low, 'GetCompressedFileSizeW'
    return info.st_size, 'logical_fallback'


def inventory(args):
    root = Path(args.root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError('The requested root must be a directory.')
    output = Path(args.output).expanduser().absolute()
    if output.exists() or output.is_symlink():
        raise ValueError('The output already exists; choose a fresh report filename.')
    start = time.monotonic()
    disk = shutil.disk_usage(root)
    device = root.stat().st_dev
    stack = [root]
    folders = {str(root): {'path': str(root), 'logical_bytes': 0, 'files': 0}}
    large = []
    seen_links = set()
    methods = collections.Counter()
    issues = []
    skipped = []
    issue_count = skip_count = file_count = directory_count = 0
    logical = unique_storage = hardlinked_paths = 0
    complete = True
    stop_reason = None

    def budget_exhausted():
        return file_count >= args.max_files or time.monotonic() - start >= args.max_seconds

    while stack and complete:
        current = stack.pop()
        if budget_exhausted():
            complete = False
            stop_reason = 'file_limit' if file_count >= args.max_files else 'time_limit'
            break
        directory_count += 1
        try:
            with os.scandir(native_path(current)) as entries:
                for entry in entries:
                    if budget_exhausted():
                        complete = False
                        stop_reason = 'file_limit' if file_count >= args.max_files else 'time_limit'
                        break
                    path = current / entry.name
                    try:
                        info = entry.stat(follow_symlinks=False)
                        if entry.is_symlink() or getattr(info, 'st_file_attributes', 0) & 0x400:
                            skip_count += 1
                            if len(skipped) < 100:
                                skipped.append({'path': str(path), 'reason': 'link_or_reparse_point'})
                            continue
                        # Windows DirEntry.stat omits device, inode and link count.
                        if os.name == 'nt':
                            info = os.stat(native_path(path), follow_symlinks=False)
                        if info.st_dev != device:
                            skip_count += 1
                            if len(skipped) < 100:
                                skipped.append({'path': str(path), 'reason': 'other_filesystem'})
                            continue
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(path)
                            continue
                        if not entry.is_file(follow_symlinks=False):
                            continue
                        file_count += 1
                        logical += info.st_size
                        allocated, method = storage_size(path, info)
                        methods[method] += 1
                        links = getattr(info, 'st_nlink', 1)
                        identity = (info.st_dev, info.st_ino) if info.st_ino else str(path)
                        if links > 1:
                            hardlinked_paths += 1
                            if identity not in seen_links:
                                unique_storage += allocated
                                seen_links.add(identity)
                        else:
                            unique_storage += allocated
                        parts = path.relative_to(root).parts
                        for depth in range(min(len(parts), args.depth + 1)):
                            parent = str(root.joinpath(*parts[:depth]))
                            row = folders.setdefault(parent, {'path': parent, 'logical_bytes': 0, 'files': 0})
                            row['logical_bytes'] += info.st_size
                            row['files'] += 1
                        if info.st_size >= args.min_file_bytes:
                            row = {'path': str(path), 'logical_bytes': info.st_size,
                                   'estimated_storage_bytes': allocated, 'storage_method': method,
                                   'links': links, 'mtime_ns': info.st_mtime_ns}
                            heapq.heappush(large, (info.st_size, file_count, row))
                            if len(large) > args.top_files:
                                heapq.heappop(large)
                    except OSError as exc:
                        issue_count += 1
                        if len(issues) < 100:
                            issues.append({'path': str(path), 'error': str(exc)})
        except OSError as exc:
            issue_count += 1
            if len(issues) < 100:
                issues.append({'path': str(current), 'error': str(exc)})

    return {
        'at': datetime.now(timezone.utc).isoformat(), 'requested_root': args.root, 'root': str(root),
        'complete': complete and issue_count == 0, 'enumeration_finished': complete,
        'stop_reason': stop_reason, 'seconds': round(time.monotonic() - start, 3),
        'volume': {'total_bytes': disk.total, 'used_bytes': disk.used, 'free_bytes': disk.free},
        'summary': {'files': file_count, 'directories_visited': directory_count,
                    'logical_file_bytes': logical, 'estimated_unique_file_storage_bytes': unique_storage,
                    'hardlinked_paths': hardlinked_paths, 'storage_methods': dict(methods)},
        'directories': sorted(folders.values(), key=lambda row: row['logical_bytes'], reverse=True),
        'large_files': [item[2] for item in sorted(large, reverse=True)],
        'issue_count': issue_count, 'issues': issues, 'skipped_count': skip_count, 'skipped': skipped,
        'limits': {'max_seconds': args.max_seconds, 'max_files': args.max_files, 'report_depth': args.depth},
        'notes': ['Parent and child directory totals overlap.',
                  'Storage estimates are not a deletion-gain guarantee; links may exist outside this root.',
                  'Links/reparse points and other filesystems are intentionally excluded.',
                  'No file contents are read and no cleanup operation is performed.'],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root')
    parser.add_argument('--output', required=True)
    parser.add_argument('--depth', type=int, default=2)
    parser.add_argument('--max-seconds', type=float, default=60)
    parser.add_argument('--max-files', type=int, default=250000)
    parser.add_argument('--min-file-bytes', type=int, default=100000000)
    parser.add_argument('--top-files', type=int, default=50)
    args = parser.parse_args()
    if args.depth < 0 or args.max_seconds <= 0 or args.max_files < 1 or args.min_file_bytes < 0 or args.top_files < 1:
        parser.error('Limits must be positive; depth and min-file-bytes may be zero.')
    if os.name == 'nt':
        import ctypes
        compressed_size = ctypes.WinDLL('kernel32', use_last_error=True).GetCompressedFileSizeW
        compressed_size.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_uint32)]
        compressed_size.restype = ctypes.c_uint32
    try:
        result = inventory(args)
        output = Path(args.output).expanduser().absolute()
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('x', encoding='utf-8') as handle:
            json.dump(result, handle, ensure_ascii=True, indent=2)
        print(json.dumps({'output': str(output), 'complete': result['complete'], **result['summary']}))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Inventory failed: {exc}\n')
