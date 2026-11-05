"""Five new regression reports and independent same-topic decision histories."""
from pathlib import Path
from unittest.mock import patch
from evaluation.contrast_review import corpus
from evaluation.decision_records.build import ROOT, commit, read, save

HERE = Path(__file__).resolve().parent
CASES = [
    ('patch-search','88f6ffc1c2','d85d7ecb80','d5addcf522','fd2fb4aa0c',[1,2],[2,3,4,5,6],[1,2,4,5],
     'The search-key change inserted a captureless regex, making $1 undef. Initial /regex search now warns and asks for the expression again. Identify either this actual failed search behavior or the capture overwrite and its triggering inserted regex.',
     'The alternative escapes commentChar metacharacters when stripping comments from manually edited hunks, not the capture used for hunk search.'),
    ('asan-preload','131b94a10a','71f26798f2','49da404070','067109a5e7',[1,2,3],[2,3,4,5],[1,2,8,11,15],
     'The glibc malloc-check preload change causes ASan test startup failure because ASan runtime is not first in the library list, specifically SANITIZE=address on glibc >=2.34. Include the failure and both sanitizer and version constraints. Leak/undefined are unaffected.',
     'The alternative improves LSAN stack traces with fast_unwind_on_malloc, not the GLIBC_TUNABLES/malloc-check preload ordering of ASan.'),
    ('email-priority','c95e3a3f0b8','c8243933c7','dd84e528a3','b996f84989',[1,2,3,4,5,6],[2,3,4,5,6],[1,2,3,4],
     'The Perl config reader takes the first rather than the last scalar key when repeated across config scopes, preferring global over local values. Preserve this direction and the conflicting/multiple-key condition.',
     'The alternative locates validation hooks with core.hooksPath, not scalar configuration precedence.'),
    ('commit-permissions','9c4d6c0297b','3491047e14','8b7e5f7972','4ef91a2d79',[1,2,3],[2,3,4,5],[1,2],
     'Updating/writing the cache tree during commit leads to duplicate insufficient-permission errors when .git/objects cannot be written. prepare_index should be quiet; prepare_to_commit should report the error. State the duplication and unwritable condition without swapping which call should be silent.',
     'The alternative iterates over slashes during cache_tree_find lookup, not the silent object-write path used by commit.'),
    ('help-spacing','1b81d8cb19d','968b1fe263','659fef199f','93de1b6999',[1,2],[2,3,4,5,6,7,8,9,10],[1,2,7,9,11],
     'Moving guide output to section-printing code adds an unintended leading newline for git help --guides or other single-section output. Describe the newline and single-section condition; not missing or duplicated guide text.',
     'The alternative changes the phrasing of help.autoCorrect warnings for unknown commands, not spacing before guide sections.'),
]

def build():
    with patch.object(corpus, 'CASE', CASES):
        rows, keys = corpus.build()
    previous = '\n'.join((ROOT/'evaluation'/p).read_text() for p in [
        'contrast_review/inputs.json','contrast_review/validation/inputs.json','role_review/inputs.json',
        'fixed_review/inputs.json','pair_selection/corpus.json'])
    for row in rows:
        k=keys[row['id']]
        assert k['report'].rsplit('/',1)[1][:10] not in previous
        # A wider citation remains a literal source interval. The semantic rubric
        # and separately inspected extracted failure decide whether it proves the result.
        k['new'].append(row['incoming']['source']['text'].split('\n\n',1)[1])
        if (k['scenario'], k['view'])==('mixed','raw'):
            if k['topic']=='email-priority':
                row['qa']='Which configuration file incorrectly won over .git/config in this regression?'
            if k['topic']=='asan-preload':
                row['qa']='Which SANITIZE setting makes the tests fail on glibc >= 2.34?'
    save(HERE/'inputs.json',rows);save(HERE/'key.json',keys)
if __name__=='__main__':build()
