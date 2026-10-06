import sys
from sma_gen import q
def noku(subj):
    return q("""select m.title from modules s join modules t on t.parent_id=s.id join modules g on g.parent_id=t.id join modules m on m.parent_id=g.id and not m.is_folder where s.title='%s' and s.parent_id=(select id from modules where title='Semua Mata Pelajaran' and parent_id is null) and m.source_module_id is null and exists (select 1 from module_labels l where l.module_id=m.id and l.kind='jenjang' and l.value ~ '^(SD|SMP|SMA)-') and not exists(select 1 from module_items b where b.module_id=m.id and b.node_type='section' and b.status<>'archived' and b.title like 'Kesalahan Umum%%') order by t.order_index,g.order_index,m.order_index""" % subj)
if __name__=="__main__":
    for s in sys.argv[1:]:
        r=noku(s); print("==",s,len(r)); print(" | ".join(r))
