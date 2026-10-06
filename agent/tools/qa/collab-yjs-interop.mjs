import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'
import WebSocket from 'ws'
import fs from 'fs'

const info = JSON.parse(fs.readFileSync(process.argv[2]))
const url = `ws://127.0.0.1:${info.port}/ws/module-items`
const room = `${info.item}/collab`
const sleep = ms => new Promise(r => setTimeout(r, ms))
function client() {
  const doc = new Y.Doc()
  const provider = new WebsocketProvider(url, room, doc, { WebSocketPolyfill: WebSocket, params: { token: info.token }, disableBc: true })
  return { doc, provider }
}
async function synced(c) { if (!c.provider.synced) await new Promise(r => c.provider.once('sync', r)) }
const fail = m => { console.error('FAIL', m); process.exit(1) }

const a = client(), b = client()
await synced(a); await synced(b)
// Text, XML (what a rich-text editor binds to) and a map, edited on both sides.
a.doc.getText('body').insert(0, 'Halo dunia')
const para = new Y.XmlElement('paragraph'); para.insert(0, [new Y.XmlText('Isi paragraf')])
a.doc.getXmlFragment('content').insert(0, [para])
a.doc.getMap('meta').set('judul', 'Bab 1')
await sleep(500)
if (b.doc.getText('body').toString() !== 'Halo dunia') fail('b text ' + b.doc.getText('body'))
b.doc.getText('body').insert(4, ' semuanya')
b.doc.getText('body').delete(0, 1)
b.doc.getMap('meta').set('level', 3)
await sleep(500)
const want = 'alo semuanya dunia'
for (const [n, c] of [['a', a], ['b', b]]) {
  if (c.doc.getText('body').toString() !== want) fail(`${n} text ${c.doc.getText('body')}`)
  if (c.doc.getXmlFragment('content').toString() !== '<paragraph>Isi paragraf</paragraph>') fail(`${n} xml ${c.doc.getXmlFragment('content')}`)
  if (c.doc.getMap('meta').get('judul') !== 'Bab 1' || c.doc.getMap('meta').get('level') !== 3) fail(`${n} map`)
}
// Awareness (cursors) reach the peer.
a.provider.awareness.setLocalStateField('user', { name: 'A' })
await sleep(400)
const seen = [...b.provider.awareness.getStates().values()].some(s => s.user && s.user.name === 'A')
if (!seen) fail('awareness')
a.provider.destroy(); b.provider.destroy()
await sleep(800) // the room empties: final checkpoint, eviction
// A later session is brought up from the stored state.
const c = client(); await synced(c); await sleep(300)
if (c.doc.getText('body').toString() !== want) fail('c text ' + c.doc.getText('body'))
if (c.doc.getXmlFragment('content').toString() !== '<paragraph>Isi paragraf</paragraph>') fail('c xml')
// ...and an edit made after reload still merges.
c.doc.getText('body').insert(0, '>')
await sleep(300)
c.provider.destroy()
await sleep(800)
console.log('OK')
fs.writeFileSync(process.argv[2] + '.done', '')
process.exit(0)
