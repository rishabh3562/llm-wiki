---
repo: meteor
type: intent_recovery
commit: 4b61fbf9b1e2364e0b6ab99fd67e2b82cf673a94
date: 2026-04-23
tags: [meteor, intent_recovery]
related: [[meteor-index]]
---
# Intent Recovery — meteor

## Timeline
- First commit: 2011-11-17
- Last commit: 2025-10-08
- Total commits: 40162

## Full Commit Log

d69c2d1f19 2011-11-17 Initial import from old busted repo. (Nick Martin)
052ebbe035 2011-11-17 Add communication mechanisms. (Nick Martin)
36f1a7cadd 2011-11-17 Fix wrong repo name. (Nick Martin)
7bd74d1b1f 2011-11-18 Bump to version 0.0.32 (Nick Martin)
f57add24a6 2011-11-18 readme tweak. (Nick Martin)
1a824caa8e 2011-11-18 strings tweak. (Nick Martin)
ec8eccfc65 2011-11-18 Add amplify package. (Nick Martin)
4a47e39ac5 2011-11-21 Stop skybreak outer process from crashing when the inner does. Not sure why this started being needed, but it fixes it. (Nick Martin)
a46c7f38c6 2011-11-21 Bump to version 0.0.33 (Nick Martin)
dc59c44942 2011-11-24 simplify publish API for tp0 (Geoff Schmidt)
760e6d5a9b 2011-11-24 use correct collection name on client (Geoff Schmidt)
f58e659095 2011-11-25 Remove support for template setup functions (Geoff Schmidt)
c814e34df8 2011-11-25 make {{> foo bar}} shorthand actually work (previously, you would get an error about a circular reference while serializing JSON) (Geoff Schmidt)
1f18d2802b 2011-11-26 comment (Geoff Schmidt)
012abe536d 2011-11-26 rename subscriptions => autosubscribe (Geoff Schmidt)
d2c3f52d9d 2011-11-26 Remove Sky.ui support for underscore templates (Geoff Schmidt)
08f9e60d71 2011-11-26 remove more _.template cruft (Geoff Schmidt)
89b4263ec1 2011-11-26 refactor Sky.deps for clarity (Geoff Schmidt)
598337d505 2011-11-26 a much simpler implementation of session (Geoff Schmidt)
7a299369b8 2011-11-28 Bump to version 0.0.34 (Nick Martin)
a13ca9e2cc 2011-11-28 Bump to version 0.0.35 (Nick Martin)
61ba3fdf36 2011-11-28 Use our version of rm -rf, not wrench's. Wrench's follows symlinks poorly! (Nick Martin)
bf61c47a0f 2011-11-28 Bump to version 0.0.36 (Nick Martin)
a6b172e0aa 2011-11-27 comment (Geoff Schmidt)
f3ee05ac06 2011-11-28 copyediting tweaks (Geoff Schmidt)
4f245840d7 2011-11-28 Do not include coffeescript by default. (Nick Martin)
3a61d00268 2011-11-28 Correct docs. (Nick Martin)
948388a430 2011-11-29 comment (Geoff Schmidt)
a277dcdf26 2011-11-29 don't output Modified message (matt debergalis)
63aa9ac5c7 2011-11-29 wrong event data was passed to renderLive events (Geoff Schmidt)
1df7d90049 2011-11-29 allow sort, skip, limit in Sky.publish (Geoff Schmidt)
ceef60fad8 2011-11-29 Bump to version 0.0.37 (Nick Martin)
3dc9e037d1 2011-11-29 Make sure to resolve path passed in to bundle, since we switch working directories when we invoke tar. (Nick Martin)
9be7026cb7 2011-11-29 send raw tarball for deploy (matt debergalis)
eed2c3288e 2011-11-29 Merge branch 'master' of github.com:skybreak/skybreak (matt debergalis)
0cbc9650fb 2011-11-29 Bump to version 0.0.38 (Nick Martin)
f57b6e1bd6 2011-11-29 Make keepalives opt-in, instead of on by default. Turn them on in dev mode. (Nick Martin)
cfbb309272 2011-12-01 shorten description (matt debergalis)
555a448e2a 2011-12-01 restyle skel (Geoff Schmidt)
aaa47bbc34 2011-12-01 comment cleanups (Geoff Schmidt)
a02f7a0137 2011-12-01 Bump to version 0.0.39 (Nick Martin)
1d4f9
## Questions To Answer
- What problem was this solving?
- What was the original architecture?
- When did maintenance drop off and why?
- What did I know when I built this?
- Why did I stop?
