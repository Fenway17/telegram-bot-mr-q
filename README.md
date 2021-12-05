# MRQ Queue System

tldr; Telegram Queue bot with waiting lists



Git Workflow SOPs:
- Release numbers will be as such: "release-\<ver>.\<feature>.\<bug>"
  - e.g. release-1.1.2 (Means 1st major release, 1st major feature, 2nd bugfix batch)
- We will start from 0.0.0 (Basically main branch will be useless but we can make main be updated to the latest version)
  - Once everyone has completed their respective cards for that release, then we will move on to the next release number
- Ensure that your commit message includes the title of the card you are working on
- There will be 3 types of properties in each card:
  - Bug
  - Feature
  - (&) Blocker
  * A card can be a bug or a feature | (bug & blocker) | (feature & blocker)
- If there are cards/issues coming in when we are about to complete our sprint, those cards will be pushed to next release
  - If a developer is unable to complete their card in time for the release, the card will also be pushed to next release, however, if the card is a blocker, the sprint will be delayed until this issue is fixed. 
