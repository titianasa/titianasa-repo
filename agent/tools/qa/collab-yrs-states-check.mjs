import * as Y from 'yjs'
import fs from 'fs'
const pairs = JSON.parse(fs.readFileSync(process.argv[2]))
let bad = 0
for (const p of pairs) {
  const a = new Y.Doc(), b = new Y.Doc()
  Y.applyUpdate(a, Buffer.from(p.Original, 'hex'))
  Y.applyUpdate(b, Buffer.from(p.Reencoded, 'hex'))
  const same = Buffer.compare(Buffer.from(Y.encodeStateVector(a)), Buffer.from(Y.encodeStateVector(b))) === 0
  const ja = JSON.stringify(a.toJSON()), jb = JSON.stringify(b.toJSON())
  if (!same || ja !== jb) { bad++; console.log('DIFF', p.ID, same, ja.length, jb.length) }
}
console.log(pairs.length, 'states,', bad, 'differences')
