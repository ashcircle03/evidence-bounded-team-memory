"""Separate procedural supervision for claim-instance attachment, never benchmark labels.

Domains are split as families. Templates vary absence, adjacent distractors,
scope, explicit rationale and a rationale shared by two independent claims.
This narrow grammar is a training pilot, not representative language coverage.
"""
import json
from pathlib import Path

from team_memory.records.learned_binding import FIELDS

TRAIN = [
 ('orchard','prune the apple trees','inspect the pear trees','the branches are dormant','winter orchards','the branches crowd the canopy','the fruit has visible blemishes'),
 ('museum','dim the gallery lamps','close the skylight','fragile paintings are on display','watercolor galleries','bright light damages the pigments','sunlight reaches the display'),
 ('bakery','extend the dough resting period','lower the oven temperature','the dough feels stiff','wholegrain loaves','the flour absorbs more water','the crust browns too quickly'),
 ('marina','secure the small boats','close the outer pier','strong tides are forecast','exposed berths','the mooring ropes are worn','waves reach the walkway'),
 ('theatre','delay the curtain rise','inspect the stage lights','the audience is still entering','evening performances','several seats remain inaccessible','a cable has become loose'),
 ('garden','cover the seed trays','move the citrus pots indoors','frost is expected','outdoor seedlings','the young shoots are delicate','the leaves show cold damage'),
 ('library','reserve the quiet room','extend the borrowing period','exams are approaching','student borrowers','the main hall is noisy','the reference book is lengthy'),
 ('pottery','reduce the kiln temperature','extend the cooling period','thin bowls are being fired','porcelain bowls','the glaze forms bubbles','rapid cooling causes cracks'),
 ('cafe','grind the beans more finely','reduce the water temperature','the coffee tastes weak','light roast beans','the extraction is too brief','the drink tastes bitter'),
 ('trail','close the ridge path','mark the forest detour','heavy rain is forecast','steep hiking routes','the soil is unstable','fallen trees block the usual route'),
 ('laundry','wash the scarves by hand','air dry the sweaters','delicate fabric is present','wool garments','machine agitation stretches the fibers','high heat causes shrinkage'),
 ('workshop','sharpen the carving tools','replace the worn clamp','hard wood is being carved','oak panels','dull blades tear the grain','the workpiece slips during cutting'),
]
DEV = [
 ('aquarium','reduce the feeding amount','clean the filter sponge','the water is cloudy','freshly stocked tanks','uneaten food fouls the water','debris restricts water flow'),
 ('darkroom','shorten the exposure time','replace the developer bath','the prints appear too dark','high contrast negatives','excess light obscures fine detail','the solution has lost strength'),
 ('orchestra','slow the rehearsal tempo','reposition the brass players','the ensemble loses synchronization','difficult passages','the musicians cannot hear the cue','the brass overwhelms the strings'),
 ('apiary','add another hive box','reduce the entrance opening','the colony grows rapidly','crowded hives','the bees need more storage space','wasps enter the hive'),
]


def make(topic, modal):
    family,a,b,c,scope,r,s=topic
    if modal: a='we propose to '+a;b='we intend to '+b
    cases=[
      (f'When {c}, {a} because {r}.',[(a,[c],[r])]),
      (f'{a} if {c}.',[(a,[c],[])]),
      (f'{r}. For this reason, {a}.',[(a,[],[r])]),
      (f'For {scope}, {a}.',[(a,[scope],[])]),
      (f'{a}. Meanwhile, {b}.',[(a,[],[]),(b,[],[])]),
      (f'If {c}, {a}. Meanwhile, {b} because {s}.',[(a,[c],[]),(b,[],[s])]),
      (f'{a} and {b} because {r}.',[(a,[],[r]),(b,[],[r])]),
      (f'{r}; therefore, {a}. Meanwhile, {b}.',[(a,[],[r]),(b,[],[])]),
      (f'{a} because {r}; {b} because {s}.',[(a,[],[r]),(b,[],[s])]),
      (f'The next instruction applies when {c}. {a}. Separately, {b}.',[(a,[c],[]),(b,[],[])]),
    ]
    for index,(text,records) in enumerate(cases):
        def span(q):
            assert text.count(q)==1,(family,index,q)
            start=text.index(q);return dict(text=q,start=start,end=start+len(q))
        output=dict(json_structures=[{'statement':dict(claim=span(x),condition=[span(q) for q in cc],basis=[span(q) for q in rr])} for x,cc,rr in records],
                    json_descriptions={'statement':FIELDS},
                    record_metadata={'statement':dict(mode='natural',anchor='claim',occurrence_policy='all',fields=dict(
                        claim=dict(cardinality='required_one'),condition=dict(cardinality='zero_or_more',exclusive=False),basis=dict(cardinality='zero_or_more',exclusive=False)))})
        yield dict(id=f'{family}-{int(modal)}-{index}',family=family,template=index,input=text,output=output)


def main():
    target=Path('evaluation/record_binding/adaptation_data');target.mkdir()
    for split,topics in [('train',TRAIN),('dev',DEV)]:
        rows=[r for t in topics for modal in [False,True] for r in make(t,modal)]
        (target/(split+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
        (target/(split+'.jsonl')).write_text(''.join(json.dumps({k:r[k] for k in ('input','output')})+'\n' for r in rows))
        print(split,len(rows))


if __name__=='__main__':main()
