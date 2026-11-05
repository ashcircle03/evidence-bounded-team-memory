"""Freeze new original-source transfer streams; no model outputs are consulted.

The paired histories are controlled constructions, not twenty independent
historical team conversations. Ten genuine follow-up reports each appear with
and without the decision they actually bear on. All actor text is verbatim Git
commit prose (standard trailers removed consistently with earlier panels).
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

from team_memory.store import digest, source_envelope
from .prepare import write

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GIT = ROOT.parent / '.work/revision-git.git'

# The quotes/rubrics below are evaluator-only. They never enter actor inputs.
SPECS = [
    dict(id='pack-validity', old='44f9fd6496', new='62b3ec8a3f',
         foils=['60980aed78', '17a4be2606'],
         old_quote='But it\'s simpler to do\nthe check as early as possible, covering all direct uses of the\npreferred pack.',
         new_quote='But 44f9fd6496 was not extended to cover multi-pack reuse, meaning that\nthis same race condition exists for non-preferred packs during verbatim\nreuse.',
         criterion='Revisit preferred-pack-only early validation because multi-pack verbatim reuse also needs valid open non-preferred packs. Preserve the original race rationale; do not claim that opening the preferred pack was itself wrong or that every pack must be opened eagerly.',
         negative_reason='Filename-buffer ownership and RGB color parsing are unaffected by validity checks for reusable pack files.',
         question='In the earlier MIDX filename allocation change, why did get_midx_filename and get_midx_rev_filename take a strbuf output parameter?',
         qa_quote='That allows us to implement the function without copying or open-coding\nget_midx_filename() in a way that doesn\'t leak.'),
    dict(id='fetch-rechecks', old='45e8a74', new='5827a03545',
         foils=['72549dfd5d', 'e7821d7'],
         old_quote='This lets us handle a process that is writing to the\nrepository simultaneously',
         new_quote='This patch teaches fetch to use HAS_SHA1_QUICK to sacrifice\naccuracy for speed, in cases where we might be racy with a\nsimultaneous repack.',
         criterion='Revisit mandatory pack-directory rechecking specifically for tag auto-following with many packs, many candidate tags and disconnected history: repeated scans are expensive and a missed tag is acceptable there. Do not remove the original correctness protection for general reachability/pruning.',
         negative_reason='Loading default configuration at fetch startup and the Windows color-output API restriction do not depend on tag-following pack-directory scan cost.',
         question='Why did the earlier fetch change load core configuration at startup even when no objects were transferred?',
         qa_quote='But if the fetch is a pure ref\nupdate (e.g., a new ref which is a copy of an old one), we\nskip fetch_pack entirely. So we get inconsistent results\ndepending on whether or not we have actual objects to\ntransfer or not!'),
    dict(id='windows-colors', old='e7821d7', new='3d0a83382f',
         foils=['17a4be2606', '35fb0e8633'],
         old_quote='We emulate color escape codes on Windows by overriding printf, fprintf,\nand fputs. Warn developers that these are the only functions that can be\nused to print them.',
         new_quote='the ANSI color sequence support\ncode needed to be replaced with a thread-safe version, one side effect\nbeing that stdout and stderr handled no matter which function is used to\nwrite to it.',
         criterion='Revisit the restriction to printf/fprintf/fputs because the later thread-safe console implementation handles stdout/stderr independently of the writing function. This is an implementation-era change, not proof the 2009 limitation was false then.',
         negative_reason='How RGB color values are parsed and how an executable prefix is resolved do not change when console output interception changes.',
         question='What color specification did the earlier parse_color change add support for?',
         qa_quote='Some terminals (like XTerm) allow full 24-bit RGB color\nspecifications using an extension to the regular ANSI color\nscheme.'),
    dict(id='maintenance-auto', old='41abfe15d9', new='9f6714ab3e',
         foils=['16c5690929', 'e258eb4800'],
         old_quote="The 'auto_condition' function pointer is left NULL for now. We could\nextend this in the future to have a condition check if pack-refs should\nbe run during 'git maintenance run --auto'.",
         new_quote='now that we do have the logic in place to let ref backends\ndecide whether or not to repack refs, it does make sense to wire it up\naccordingly.',
         criterion='Revisit leaving pack-refs auto_condition unset now that ref backends can decide whether to repack. The new reftable auto-compaction support is relevant; do not claim the files backend already has an automatic threshold heuristic.',
         negative_reason='Documenting cron schedules and keeping progress output on stderr are independent of the pack-refs auto-condition callback.',
         question='Why were cron details added to the earlier git maintenance documentation?',
         qa_quote="Advanced and expert users may want to know how 'git maintenance start'\nschedules background maintenance in order to customize their own\nschedules beyond what the maintenance.* config values allow."),
    dict(id='end-of-options', old='51b4594b40', new='9385174627',
         foils=['5f0df44cd7', 'e258eb4800'],
         old_quote='We can even piggy-back on the\nhandling of PARSE_OPT_KEEP_DASHDASH, because any caller that wants to\nretain one will want to retain the other.',
         new_quote='But that turned out miss quite a few cases that pass KEEP_DASHDASH but\ndo their own manual parsing.',
         criterion='Revisit equating retention of --end-of-options with KEEP_DASHDASH after reset/checkout-style manual parsers demonstrate the assumption fails. KEEP_UNKNOWN_OPT tracks continued option parsing. Do not reverse the flag roles or claim stopping option parsing should disappear.',
         negative_reason='Formatting argument-help placeholders and stdout/stderr documentation do not control which end-of-options tokens are retained in argv.',
         question='When did the earlier parse-options change stop adding angular brackets around argument help strings?',
         qa_quote="Stop adding these angular brackets if special characters are present,\nas they indicate that we don't deal with a simple placeholder."),
    dict(id='perforce-install', old='5ed9fc3fc86', new='d1c9195116',
         foils=['176441bfb5', '16c5690929'],
         old_quote="Let's ask Homebrew specifically to _not_ quarantine the Perforce\nbinaries.",
         new_quote="Perfoce's cask in brew is meant[1] to be used only by humans, so replace\nits use from the CI with a scripted binary download which is less likely\nto fail, as it is done in Linux.",
         criterion='Revisit Homebrew-based non-quarantined Perforce installation because the cask is unsuitable for unattended CI. A scripted download is proposed, but quarantine risk returns and is explicitly deferred; do not say SIP or the old hang has been solved by downloading.',
         negative_reason='The Perforce cask restriction is not a ban on Homebrew GCC installation, and it does not change Git maintenance cron documentation.',
         question='Which GCC version did the earlier osx-gcc CI change install and link explicitly, and why pin it?',
         qa_quote="Install 'gcc@9' specifically, so we'll still get what we want even\n    after GCC 10 comes out, and the \"plain\" 'gcc' package starts to\n    refer to 'gcc@10'."),
    dict(id='threeway-binary', old='923cd87ac8', new='57f183b698',
         foils=['eb3c027e17', '72549dfd5d'],
         old_quote='when "--3way" is used,\ngit will always try the three-way merge first and\nwill only fall back to apply_fragments() in cases\nwhere blobs are not available or some other error',
         new_quote='This no longer is true after we made "--3way" to mean "first try\nthree-way and then fall back to straight application", and made\n"git apply -3" on a binary patch that is based on the current\nversion no longer apply.',
         criterion='Revisit the three-way-first application path for trivial binary merges: ll_binary_merge assumes neither side equals the ancestor because normal callers resolve trivial cases first. Check trivial cases before the driver; do not claim the report calls for globally reverting three-way-first or changing directory permissions.',
         negative_reason='Working-tree directory permissions and fetch configuration loading are not affected by trivial binary merge resolution.',
         question='According to the earlier apply permissions change, should core.sharedRepository affect files created in the working tree?',
         qa_quote="core.sharedRepository defines which permissions Git should set when\ncreating files in $GIT_DIR, so that the repository may be shared with\nother users. But (in its current form) the setting shouldn't affect how\nfiles are created in the working tree."),
    dict(id='runtime-prefix', old='35fb0e8633', new='226c0ddd0d',
         foils=['8252df6218', '17a4be2606'],
         old_quote='On Unix, further work is required before\nRUNTIME_PREFIX can be enabled.',
         new_quote='This is used to enable RUNTIME_PREFIX support for non-Windows systems,\nnotably Linux and Darwin.',
         criterion='Revisit the Windows-only availability restriction after executable-path discovery is implemented for Linux/Darwin/BSD and absolute argv0. Do not claim runtime-prefix becomes the default on all Unix systems, or that all path discovery is guaranteed rather than best effort.',
         negative_reason='Removing an unused stat device field and parsing RGB colors do not depend on enabling relocatable executable-prefix support on POSIX.',
         question='Why did the earlier mingw lstat/fstat change remove _getdrive usage?',
         qa_quote='The field device is not used by Git, and putting the number of the\ncurrent device is meaningless anyway.'),
    dict(id='c99-deadline', old='6563706568', new='82dd01d81b',
         foils=['e258eb4800', '5b1cd37e44'],
         old_quote='we will officially adopt the variable declaration\nin the initializaiton part of "for ()" statement this winter, unless\nwe find that a platform we care about does not grok it.',
         new_quote="As November 2022 is within the window of this upcoming release,\nlet's update the guideline to allow this.",
         criterion='Revisit the pending for-loop declaration guideline because the agreed time window has arrived and releases have already exercised the construct. The report still allows discussion/drop if premature; do not invent proof that every platform was tested or treat this record as an owner approval in the simulated service.',
         negative_reason='Permission for C99 for-loop declarations changes neither output-stream conventions nor guidance about gender-neutral descriptions.',
         question='According to the earlier CodingGuidelines record, where should primary output and chatty progress messages go?',
         qa_quote='a command to emit its\nprimary output to stdout so that it can be captured to a file or sent\ndown a pipe, and to emit "chatty" messages (such as those reporting\nprogress) to stderr so that they don\'t interfere with the primary\noutput.'),
    dict(id='bitmap-to-file', old='6b8fda2d', new='645c432d61',
         foils=['781d93067d', '72549dfd5d'],
         old_quote='We must be packing to stdout (as a normal `pack-objects` from\n     `upload-pack` would do).',
         new_quote='One might want to generate on-disk\n    packfiles for a specialized object transfer.',
         criterion='Revisit the stdout-only bitmap traversal restriction for specialized on-disk transfer packs with an explicit --use-bitmap-index opt-in. Retain the robust default for git repack and the distinction between bitmap traversal and verbatim pack reuse; do not claim all on-disk repacks or all pack reuse should be enabled.',
         negative_reason='Allocating sorted_by_pos for ref deltas and loading fetch configuration are independent of enabling bitmap traversal for explicit on-disk transfers.',
         question='Why was nr_unresolved an unsuitable allocation count for sorted_by_pos in the earlier index-pack fix?',
         qa_quote='The code allocated an array\nfor nr_unresolved, which is sum of number of ref- and ofs-deltas\nminus nr_resolved, which may be larger or smaller than the number\nref-deltas.')
]


def original(rev):
    raw = subprocess.check_output(['git','--git-dir',str(GIT),'show','-s',
        '--format=%H%x00%cI%x00%an%x00%B',rev], text=True).strip()
    oid, when, author, message = raw.split('\0',3)
    prose = re.split(r'(?im)^(?:[\w-]+-by|Cc|Link):\s',message)[0].strip()
    env = source_envelope(dict(owner=author,observed_at=when,
        source=dict(speaker=author,location='https://github.com/git/git/commit/'+oid,text=prose)))
    return env, dict(commit=oid,raw_message_sha256=sha256(message.encode()).hexdigest(),
                    source_text_sha256=sha256(prose.encode()).hexdigest(),
                    projection='Full commit subject/body; standard trailing attribution/link block removed')


def witness(env, quote):
    text = env['source']['text']; start = text.index(quote)
    return dict(source_id=digest(env),start=start,end=start+len(quote),quote=quote,
                location=env['source']['location'])


def exclusion_audit(originals):
    # Only prior actor/evaluation artifacts. Never inspect final model outputs.
    files = [p for p in (ROOT/'evaluation').rglob('*') if p.suffix in ('.json','.py')
             and p != Path(__file__) and not p.name.startswith('transfer')
             and p.name not in ('final-data-freeze.json',)]
    matched = []
    for p in files:
        text = p.read_text(errors='replace')
        for source, _ in originals.values():
            oid = source['source']['location'].rsplit('/',1)[-1]
            # URLs, quoted commit IDs, and source prose all identify prior use.
            if oid in text or re.search(r'(?<![a-zA-Z0-9])'+oid[:10]+r'(?![a-zA-Z0-9])',text):
                matched.append(dict(path=str(p.relative_to(ROOT)),commit=oid))
    if matched: raise RuntimeError('Previously used source events: '+json.dumps(matched))
    return dict(prior_artifact_count=len(files),matches=matched,
                files_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sorted(files)})


def build():
    runtime=json.loads((HERE/'final-runtime-freeze.json').read_text())
    assert all(sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in runtime['files_sha256'].items())
    originals={rev:original(rev) for s in SPECS for rev in [s['old'],s['new'],*s['foils']]}
    audit=exclusion_audit(originals)
    actor=dict(scope='Controlled source-grounded transfer:20 paired histories from10 independent genuine Git follow-ups; original text, no manual claim labels',cases=[])
    key=dict(audience='evaluator_only',positive_required=8,negative_proposals_allowed=0,
             paired_reports=10,stream_count=20,cases={})
    for spec in SPECS:
        old,new=[originals[spec[k]][0] for k in ('old','new')]
        foils=[originals[r][0] for r in spec['foils']]
        assert all(datetime.fromisoformat(x['observed_at'])<datetime.fromisoformat(new['observed_at']) for x in [old,*foils])
        # Require actual immutable ancestry as well as timestamps for the target.
        subprocess.run(['git','--git-dir',str(GIT),'merge-base','--is-ancestor',spec['old'],spec['new']],check=True)
        for positive in (True,False):
            cid=spec['id']+('-present' if positive else '-absent')
            prior=[old,foils[0]] if positive else list(foils)
            prior.sort(key=lambda x:(x['observed_at'],digest(x)))
            actor['cases'].append(dict(id=cid,events=[
                dict(label='history',operation='import_history',records=prior),
                dict(label='new_report',operation='ingest',source=new),
                dict(label='retained_fact',operation='ask',question=spec['question'],temporal_scope='historical')]))
            key['cases'][cid]=dict(independent_report=spec['id'],positive=positive,
                actual_target=digest(old) if positive else None,incoming=digest(new),
                expected='reconsider' if positive else 'no_consequential_proposal',
                criterion=spec['criterion'] if positive else spec['negative_reason'],
                old_witness=witness(old,spec['old_quote']) if positive else None,
                new_witness=witness(new,spec['new_quote']),
                foil_source_ids=[digest(f) for f in foils],
                qa=dict(question=spec['question'],evidence=witness(foils[0],spec['qa_quote'])))
    # Interleave present/absent across two equal partitions without changing rows.
    write(HERE/'transfer.json',actor);write(HERE/'transfer-key.json',key)
    for part,case_ids in [('a',range(0,10)),('b',range(10,20))]:
        write(HERE/f'transfer-{part}.json',dict(scope=actor['scope'],cases=[actor['cases'][i] for i in case_ids]))
    write(HERE/'transfer-provenance.json',dict(originals={rev:meta for rev,(_,meta) in originals.items()},
        novelty=audit, limitations=[
            '20 controlled histories reuse10 incoming reports; paired negatives are not independent natural incidents.',
            'Final histories are short two-source collections followed by one new report, not long-running production repositories.',
            'Some incoming original commits explicitly cite earlier commits, making candidate matching easier.',
            'Historical changes are replayed as unapproved incoming source records. Commit authors stand in for source owners; no claim about historical PR approval.',
            'Negative histories intentionally omit the true target and contain a same-topic but unaffected prior plus another unaffected source.',
            'Two cases concern explicit policy/capability reconsideration rather than an observed runtime failure.',
            'This is not an official STALE or EverMemBench benchmark.']))
    paths=['transfer.json','transfer-key.json','transfer-a.json','transfer-b.json','transfer-provenance.json','transfer.py','final-runtime-freeze.json']
    freeze=dict(frozen_at=datetime.now(timezone.utc).isoformat(),stage='Before any transfer model inference',
                actor_has_gold=False,streams=20,positive=10,negative=10,independent_incoming_reports=10,
                files_sha256={p:sha256((HERE/p).read_bytes()).hexdigest() for p in paths})
    write(HERE/'final-data-freeze.json',freeze)
    return {k:v for k,v in freeze.items() if k!='files_sha256'}


if __name__=='__main__': print(json.dumps(build(),indent=2))
