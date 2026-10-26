#!/usr/bin/env node
// Ajoute une ligne à l'événement « À faire » du jour (journée entière, agenda principal).
// Usage : node note-agenda.mjs YYYY-MM-DD "ligne"   (date omise = aujourd'hui, fuseau NOTE_AGENDA_TZ ou celui de la machine)
import { execFileSync } from 'node:child_process';

const GWS = process.env.GWS || 'gws';
const args = process.argv.slice(2);
const date = /^\d{4}-\d{2}-\d{2}$/.test(args[0] || '') ? args.shift()
  : new Date().toLocaleDateString('sv-SE', { timeZone: process.env.NOTE_AGENDA_TZ || Intl.DateTimeFormat().resolvedOptions().timeZone });
const line = args.join(' ').trim();
if (!line) { console.error('usage: note-agenda.mjs [YYYY-MM-DD] "ligne"'); process.exit(1); }

const gws = (...a) => JSON.parse(execFileSync(GWS, a, { encoding: 'utf8', shell: process.platform === 'win32' }));
const q = s => process.platform === 'win32' ? `"${s.replace(/"/g, '\\"')}"` : s;

const next = new Date(`${date}T12:00:00Z`); next.setUTCDate(next.getUTCDate() + 1);
const end = next.toISOString().slice(0, 10);
const found = gws('calendar', 'events', 'list', '--params', q(JSON.stringify({
  calendarId: 'primary', timeMin: `${date}T00:00:00Z`, timeMax: `${end}T00:00:00Z`,
  singleEvents: true, privateExtendedProperty: 'noteAgenda=1' })))
  .items.filter(e => e.start?.date === date);

const bullet = `• ${line}`;
let ev;
if (found.length) {
  const cur = found[0];
  const desc = cur.description ? `${cur.description}\n${bullet}` : bullet;
  ev = gws('calendar', 'events', 'patch', '--params', q(JSON.stringify({ calendarId: 'primary', eventId: cur.id })),
    '--json', q(JSON.stringify({ description: desc })));
} else {
  ev = gws('calendar', 'events', 'insert', '--params', q(JSON.stringify({ calendarId: 'primary' })),
    '--json', q(JSON.stringify({
      summary: 'À faire', description: bullet, transparency: 'transparent',
      start: { date }, end: { date: end },
      extendedProperties: { private: { noteAgenda: '1' } } })));
}
console.log(JSON.stringify({ id: ev.id, date: ev.start.date, description: ev.description, link: ev.htmlLink }, null, 1));
