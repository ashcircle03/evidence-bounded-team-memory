from evaluation.record_groups.evaluate import covers,probe


def test_coverage_requires_all_nonspace_characters_and_an_actual_occurrence():
    text='go under ice'
    assert covers(text,'under ice',[{'start':3,'end':8},{'start':9,'end':12}])
    assert not covers(text,'under ice',[{'start':3,'end':7},{'start':9,'end':12}])
    assert not covers(text,'missing',[{'start':0,'end':len(text)}])


def test_presence_in_other_claim_does_not_satisfy_binding():
    text='run A on ice. run B on sand.'
    units=[dict(id='a',start=0,end=5),dict(id='ice',start=6,end=12),dict(id='b',start=14,end=19),dict(id='sand',start=20,end=27)]
    source=dict(text=text,record_graph=dict(status='annotated',units=units,claims=[dict(id='a',claim=['a'],condition=['sand'],basis=[]),dict(id='b',claim=['b'],condition=['ice'],basis=[])]))
    p=dict(source_id='x',anchor='run A',condition=['on ice'],basis=[],absent=[],forbidden=['on sand'])
    row=probe(source,p)
    assert not row['passed'] and row['negative_role_violation']
