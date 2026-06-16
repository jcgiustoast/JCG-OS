## Architecture

```
JCG-OS/
├── CLAUDE.md                # This file — root schema
├── life/                    # Space 1: Professional & Personal
│   ├── wiki/
│   │   ├── life-index.md    #   Master catalog for life/
│   │   ├── identity.md      #   Who Juan is
│   │   ├── professional.md  #   Mars Men context, role, team
│   │   ├── projects.md      #   Personal/side projects
│   │   ├── strategy.md      #   1-5 year plan, financial targets
│   │   └── learning.md      #   Active learning tracks
│   ├── raw/                 #   Immutable sources
│   │   ├── articles/
│   │   ├── notes/
│   │   ├── screenshots/
│   │   └── data/
│   └── memory/
│       ├── log.md           #   Chronological activity log
│       └── wiki.md          #   Compiled knowledge topics
├── content/                 # Space 2: Content & Exploration
│   ├── wiki/
│   │   ├── content-index.md  #   Master catalog for content/
│   │   ├── content-strategy.md # Phased content plan (bridges both spaces)
│   │   └── ...              #   Topic pages, content ideas
│   ├── raw/
│   │   ├── articles/        #   Reference material
│   │   ├── references/      #   Inspiration, examples
│   │   └── drafts/          #   Work-in-progress drafts
│   └── memory/
│       └── log.md           #   Content activity log
├── SETUP.md
└── .gitignore
```
