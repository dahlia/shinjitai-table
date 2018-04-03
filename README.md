Shinjitai (新字体) table
========================

[![Build status][travis-ci-badge]][travis-ci]

This repository contains two JSON files to map shinjitai (新字体) characters
to kyūjitai (舊字體) characters, and vice versa.  The data source is from
the [Jōyō Kanji Table][1] (常用漢字表) from the Agency for Cultural Affairs
(文化庁) of Japan.

[travis-ci-badge]: https://travis-ci.org/dahlia/shinjitai-table.svg?branch=master
[travis-ci]: https://travis-ci.org/dahlia/shinjitai-table
[1]: http://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/kanji/joyokanjisakuin/


*kyujitai.json*: Kyūjitai to shinjitai table
--------------------------------------------

The *kyujitai.json* file contains a large table as an JSON object.  The keys
are kyūjitai characters (e.g., `"體"`) and each value is its corresponding
shinjitai character (e.g., `"体"`) or `null` if it's the same form to the
kyūjitai one (e.g., `"字": null`).

Note that, since some shinjitai characters merged multiple kyūjitai characters
into a single character, there are duplicated shinjitai values across different
kyūjitai keys.

The kyūjitai keys of this table only consist of characters in the Jōyō Kanji
Table.


*shinjitai.json*: Shinjitai to kyūjitai table
---------------------------------------------

The *shinjitai.json* file contains a large table as an JSON object.  The keys
are shinjitai characters (e.g., `"弁"`) and each value is an array of its
corresponding kyūjitai characters (e.g., `["辨", "瓣", "辯"]`) or `null`
if it's the same form to the shinjitai one (e.g., `"字": null`).  Every value
must not be an empty array or contain the same character form to the shinjitai
key.
