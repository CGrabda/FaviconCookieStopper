# FaviconCookieStopper
The Favicon Cookie Stopping Script

---

<!-- TOC -->

- [How to use](#How-to-use)
- [Motivation](#motivation)
- [Features](#features)
- [Team](#team)

<!-- /TOC -->

## How to Use

1. Download this repository
2. Run startup.py and enter the necessary information
3. Whitelist custom links as desired in Whitelist.ini
4. Run the python script 'BookmarkedFaviconsOnly'

## Motivation

Favicons are no stranger to being used maliciously and just last month a paper was published how they can be used to create a unique tracking identifier. [SuperCookie.me](https://supercookie.me/workwise) has a demonstration of this and an explanation of how it works. [Here](https://www.cs.uic.edu/~polakis/papers/solomos-ndss21.pdf) is the acedemic paper exposing the matter.

As a cybersecurity major, I don't like tracking!

## Features and notes

- Deletes favicons except for bookmarked url's
- Has Whitelist file to add custom URL's that are not bookmarked
- Executes on run, I recommend using Task Scheduler automate to run on login
- Make sure your browser is closed before running, else nothing will occur
- Currently implemented on Edge and Chrome

## Team

| [![Christopher Grabda](https://github.com/CGrabda.png?size=100)](https://github.com/CGrabda) |
| -------------------------------------------------------------------------------------------- |
| [Christopher Grabda](https://www.linkedin.com/in/christopher-grabda/)                        |
