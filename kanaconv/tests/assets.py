# coding=utf8
#
# (C) 2015-2016, MIT License

'''
Contains word lists for our tests.
'''
# Tests whether the 'n' before vowels and y is converted
# to 'n\'' (including apostrophe).
# In traditional Hepburn, the 'n' becomes an 'm' before labial consonants,
# but this is no longer the case in modified Hepburn.
tests_apostrophe = [
    (u'しんよう', u'shin\'yō'),
    (u'かんい', u'kan\'i'),
    (u'ぐんま', u'gunma')
]

# Tests whether we're correctly running pre-processing transformations.
# These take place before we run the regular transliteration algorithm.
tests_preprocessing = [
    # transform fullwidth rōmaji to standard Latin characters
    (u'オールＡ', u'ōruA'),
    (u'ＡＢＣＤＥＦＧＨＩ', u'ABCDEFGHI'),
    (u'ＪＫＬＭＮＯＰＱＲ', u'JKLMNOPQR'),
    (u'ＳＴＵＶＷＸＹＺ１', u'STUVWXYZ1'),
    (u'２３４５６７８９０', u'234567890'),
    (u'ａｂｃｄｅｆｇｈｉ', u'abcdefghi'),
    (u'ｊｋｌｍｎｏｐｑｒ', u'jklmnopqr'),
    (u'ｓｔｕｖｗｘｙｚ', u'stuvwxyz'),
    (u'￠￡￥￦＠＃＄％＆＊＋－', u'¢£¥₩@#$%&*+-'),
    (u'０１２３４５６７８９', u'0123456789'),
    # ヿ is a ligature for コト
    (u'ヿ', u'koto'),
    # unusual (non-existent?) combination but theoretically possible
    (u'ヿー', u'kotō'),
    # ゟ is a ligature for より
    (u'えきゟ', u'ekiyori'),
    (u'えきゟい', u'ekiyorii'),
    (u'えきゟー', u'ekiyorī'),
    # check the usage of the archaic repeater characters
    (u'サヽエ', u'sasae'),
    (u'サヾエ', u'sazae'),
    (u'サゝエ', u'sasae'),
    (u'サゞエ', u'sazae'),
    (u'あひゞき', u'ahibiki'),
    # using a dakuten repeater on a non-dakuten character (simply repeat it)
    (u'まゞエ', u'mamae'),
    # check the usage of the ゠ character (for dashes in proper names)
    (u'ラッセル゠アインシュタイン', u'rasseru-ainshutain'),
    # check whether combining (han)dakuten characters are converted
    (u'か\u3099か', u'gaka'),
    (u'は\u309aは', u'paha'),
    (u'か゛か', u'gaka'),
    (u'は゜は', u'paha'),
    # when using a (han)dakuten on a non-dakuten character (simply repeat it)
    (u'わ\u3099か', u'waka'),
    (u'わ\u309aは', u'waha'),
    (u'わ゛か', u'waka'),
    (u'わ゜は', u'waha'),
    # punctuation checks
    (u'わ｛ぁ｝あ', u'wa {a} a'),
    (u'わ（ぁ）あ', u'wa (a) a'),
    (u'わ〔ぁ〕あ', u'wa [a] a'),
    (u'わ［ぁ］あ', u'wa [a] a'),
    (u'わ【ぁ】あ', u'wa [a] a'),
    (u'わ〈ぁ〉あ', u'wa <a> a'),
    (u'わ《ぁ》あ', u'wa «a» a'),
    (u'わ《ぁ》あ', u'wa «a» a'),
    (u'わ「ぁ」あ', u'wa [a] a'),
    (u'わ『ぁ』あ', u'wa [a] a'),
    (u'わ、あ', u'wa, a'),
    (u'わ＜ぁ＞あ', u'wa<a>a'),
    (u'わ＝あ', u'wa=a'),
    (u'ソン＂あ＂ソン', u'son "a" son'),
    (u'ソン＇あ＇ソン', u'son \'a\' son'),
    (u'ソン＂あソン', u'son " ason'),
    (u'わ，あ', u'wa, a'),
    (u'わ　あ', u'wa a'),
    (u'わ｀あ', u'wa`a'),
    (u'＼＾＿＾／', u'\^_^/'),
    (u'わ￤あ', u'wa¦a'),
    (u'わ￢あ', u'wa¬a'),
    (u'わ￣あ', u'wa¯a'),
    (u'わ〜あ', u'wa~a'),
    (u'わ：あ', u'wa: a'),
    (u'わ；あ', u'wa; a'),
    (u'わ：：あ', u'wa:: a'),
    (u'わ；；あ', u'wa;; a'),
    (u'わ！？あ', u'wa!? a'),
    (u'わ。あ', u'wa. a'),
    (u'わ！。あ', u'wa!. a'),
    (u'わ？！。あ', u'wa?!. a'),
    (u'わ？！。。あ', u'wa?!.. a'),
    (u'わ。？！。。あ', u'wa.?!.. a'),
    (u'わ．あ', u'wa. a'),
    (u'わ‥あ', u'wa..a'),
    (u'マイケル・シクマ', u'maikeru shikuma'),
    # some combinations with unknown characters
    (u'わぁわぁ]', u'wāwā]'),
    (u'いぁいぁ]', u'iaia]')
]

# Tests for rare and (mostly) obsolete characters and special combinations.
tests_rare_exc = [
    # ウェ is preferred for 'we'
    (u'ウェスト', u'wesuto'),
    # ウィ is 'wi', and fullwidth rōmaji is transliterated into latin
    (u'ウィンドウズＸＰ', u'windōzuXP'),
    (u'ウィーナー', u'wīnā'),
    (u'アーウィン', u'āwin'),
    # ウァ is 'va'
    (u'ウァレンティヌス', u'varentinusu'),
    # ウォ is 'wo'
    (u'ウォッシュ', 'wosshu'),
    # this one is very tricky: ク + ウ normally means 'kū', but after the
    # ォ is added we need to make sure we interpret the ウ as 'w', not 'u'
    (u'バックウォーター', u'bakkuwōtā'),
    # ヴェ is used for 've'
    (u'アヴェニュー', u'avenyū'),
    (u'クヴェ', u'kuve'),
    # ヹ is sometimes (very rarely) used instead of ヴェ
    (u'アヹ', u'ave'),
    # ヴィ is 'vi'
    (u'ヴィタミン', u'vitamin'),
    (u'ゔぃたみん', u'vitamin'),
    # ヸ is a rare form of ヴィ
    (u'アンヸル', u'anviru'),
    # ヴァ is 'va'
    (u'リーヴァル', u'rīvaru'),
    # ヷ is a rare variant of ヴァ, and is now unused
    (u'リーヷル', u'rīvaru'),
    # note: Sevastopol, normally セヴァストポリ
    (u'セヷストーポリ', u'sevasutōpori'),
    # ヴォ is 'vo'
    (u'ヴォドカ', u'vodoka'),
    # ヺ is a rare variant of ヴォ, and is now unused
    (u'インヺイス', u'invoisu'),
    # note: nouveau, normally ヌーヴォー
    (u'ヌーヺー', u'nūvō'),
    # ヮ acts just like a regular ワ; this is normally シークワーサー
    (u'シークヮーサー', u'shīkuwāsā'),
    # 島豚, of which this is an alternate Okinawan reading
    (u'シマウヮー', u'shimauwā'),
    # ゑ is technically 'we' (sometimes 'ye'), but is used as though it's 'e'
    (u'ゑびす', u'ebisu'),
    (u'ヱビス', u'ebisu'),
    # ゐ was originally 'wi', but later became considered identical to 'i'
    (u'よゐこ', u'yoiko'),
    # ヰ (katakana) is a particularly troublesome letter--it can be
    # 'i', or 'wi', or 'vi' depending on the word--but we consider
    # it to be 'i' in all cases
    (u'スヰーデン', u'suīden'),
    # rare version of ウイスキー
    (u'ウヰスキー', u'uisukī'),
    # archaic ligature for 'koto'
    (u'スルヿ', u'surukoto'),
    # small 'ka' and 'ke', though both are pronounced as 'ka'
    (u'ゕーゖーヵーヶー', u'kākākākā'),
    # a ッ before a vowel has no effect
    (u'ッアッエッカ', u'aekka'),
    # A long vowel marker that appears before any character it could
    # affect should be ignored.
    (u'ーテー', u'tē')
]

# Tests whether the word border character, '|', correctly
# prevents rōmaji long vowels from showing up.
tests_word_border = [
    (u'ぬれ|えん', u'nureen'),
    # in case the separator is missing
    (u'ぬれえん', u'nurēn'),
    (u'こ|おどり', u'koodori'),
    (u'まよ|う', u'mayou'),
    # 古往今来 (= in all ages; since antiquity)
    (u'こ|おう|こん|らい', u'koōkonrai'),
    # 小桶 (= small bucket)
    (u'こ|おけ', u'kooke'),
    # 小女 (= young woman)
    (u'こ|おんな', u'koonna'),
    # 小数点 (= decimal point)
    (u'しょう|すう|てん', u'shōsūten'),
    # the last 'u' is not converted to 'ū'
    (u'く|う', u'kuu')
]

# Tests hiragana and katakana long vowels.
tests_long_vowels = [
    (u'がっこう', u'gakkō'),
    # not kīro; i + i does not yield a long vowel
    (u'きいろ', u'kiiro'),
    (u'セーラー', u'sērā'),
    (u'おねえさん', u'onēsan'),
    (u'こおり', u'kōri'),
    (u'スーパーマン', u'sūpāman'),
    (u'とうきょう', u'tōkyō'),
    (u'パーティー', u'pātī'),
    (u'シーチキン', u'shīchikin'),
    (u'メロディー', u'merodī')
]

# Tests hiragana and katakana small vowels, including unusual
# combinations.
tests_xvowels = [
    (u'しょ', u'sho'),
    (u'しゅ', u'shu'),
    (u'しゃ', u'sha'),
    (u'ショー', u'shō'),
    (u'シュー', u'shū'),
    (u'シャー', u'shā'),
    (u'ニョ', u'nyo'),
    (u'ニュ', u'nyu'),
    (u'ニャ', u'nya'),
    (u'リャ', u'rya'),
    # チェ is used for 'che', which is chiefly katakana
    (u'チェコきょうわこく', u'chekokyōwakoku'),
    # some unusual combinations:
    (u'ワァ', u'wā'),
    (u'ワァィ', u'wāi')
]

# Tests the usage of a small ッ in front of チ and ツ.
tests_xtsu_chi = [
    (u'まっちゃ', u'matcha'),
    (u'ぼっちゃん', u'botchan'),
    (u'ボッチャン', u'botchan'),
    # mixture of hiragana and katakana
    (u'ボっチゃン', u'botchan'),
    (u'こっち', u'kotchi'),
    (u'みっつ', u'mittsu'),
]

# Tests the 1000 most frequent lemmas as determined by Wikipedia.
# See the full list and more information here: <http://is.gd/SMXdY1>
tests_freq1000 = [
    # 1. の
    (u'の', u'no'),
    # 2. に
    (u'に', u'ni'),
    # 3. する
    (u'する', u'suru'),
    # 4. は
    (u'は', u'ha'),
    # 5. を
    (u'を', u'wo'),
    # 6. た
    (u'た', u'ta'),
    # 7. が
    (u'が', u'ga'),
    # 8. 年
    (u'ねん', u'nen'),
    # 9. と
    (u'と', u'to'),
    # 10. て
    (u'て', u'te'),
    # 11. で
    (u'で', u'de'),
    # 12. だ
    (u'だ', u'da'),
    # 13. れる
    (u'れる', u'reru'),
    # 14. 月
    (u'がつ', u'gatsu'),
    # 15. いる
    (u'いる', u'iru'),
    # 16. ある
    (u'ある', u'aru'),
    # 17. 日
    (u'か', u'ka'),
    # 18. も
    (u'も', u'mo'),
    # 19. から
    (u'から', u'kara'),
    # 20. なる
    (u'なる', u'naru'),
    # 21. ない
    (u'ない', u'nai'),
    # 22. こと
    (u'こと', u'koto'),
    # 23. 第
    (u'だい', u'dai'),
    # 24. として
    (u'として', u'toshite'),
    # 25. や
    (u'や', u'ya'),
    # 26. 市
    (u'いち', u'ichi'),
    # 27. 県
    (u'けん', u'ken'),
    # 28. 者
    (u'しゃ', u'sha'),
    # 29. など
    (u'など', u'nado'),
    # 30. 日本
    (u'にほん', u'nihon'),
    # 31. 人
    (u'じん', u'jin'),
    # 32. ため
    (u'ため', u'tame'),
    # 33. 駅
    (u'えき', u'eki'),
    # 34. この
    (u'この', u'kono'),
    # 35. 的
    (u'てき', u'teki'),
    # 36. られる
    (u'られる', u'rareru'),
    # 37. その
    (u'その', u'sono'),
    # 38. 町
    (u'まち', u'machi'),
    # 39. へ
    (u'へ', u'he'),
    # 40. 後
    (u'あと', u'ato'),
    # 41. まで
    (u'まで', u'made'),
    # 42. よう
    (u'よう', u'yō'),
    # 43. 放送
    (u'ほう|そう', u'hōsō'),
    # 44. 号
    (u'ごう', u'gō'),
    # 45. 名
    (u'な', u'na'),
    # 46. 中
    (u'じゅう', u'jū'),
    # 47. という
    (u'という', u'toiu'),
    # 48. また
    (u'また', u'mata'),
    # 49. もの
    (u'もの', u'mono'),
    # 50. 行う
    (u'おこなう', u'okonau'),
    # 51. 一
    (u'ひと', u'hito'),
    # 52. 回
    (u'かい', u'kai'),
    # 53. 部
    (u'ぶ', u'bu'),
    # 54. 時
    (u'じ', u'ji'),
    # 55. 家
    (u'や', u'ya'),
    # 56. か
    (u'か', u'ka'),
    # 57. リンク
    (u'リンク', u'rinku'),
    # 58. 村
    (u'むら', u'mura'),
    # 59. 郡
    (u'ぐん', u'gun'),
    # 60. 学校
    (u'がっこう', u'gakkō'),
    # 61. より
    (u'より', u'yori'),
    # 62. できる
    (u'できる', u'dekiru'),
    # 63. 線
    (u'せん', u'sen'),
    # 64. おる
    (u'おる', u'oru'),
    # 65. 昭和
    (u'しょう|わ', u'shōwa'),
    # 66. 東京
    (u'とう|きょう', u'tōkyō'),
    # 67. 番組
    (u'ばんぐみ', u'bangumi'),
    # 68. 大
    (u'おお', u'ō'),
    # 69. により
    (u'により', u'niyori'),
    # 70. 会
    (u'え', u'e'),
    # 71. 外部
    (u'がいぶ', u'gaibu'),
    # 72. 現在
    (u'げんざい', u'genzai'),
    # 73. 画像
    (u'がぞう', u'gazō'),
    # 74. ぬ
    (u'ぬ', u'nu'),
    # 75. 区
    (u'く', u'ku'),
    # 76. による
    (u'による', u'niyoru'),
    # 77. 二
    (u'に', u'ni'),
    # 78. 国
    (u'くに', u'kuni'),
    # 79. テレビ
    (u'テレビ', u'terebi'),
    # 80. 世界
    (u'せかい', u'sekai'),
    # 81. 関連
    (u'かんれん', u'kanren'),
    # 82. 三
    (u'サン', u'san'),
    # 83. 化
    (u'か', u'ka'),
    # 84. せる
    (u'せる', u'seru'),
    # 85. 前
    (u'さき', u'saki'),
    # 86. 映画
    (u'えいが', u'eiga'),
    # 87. によって
    (u'によって', u'niyotte'),
    # 88. 作品
    (u'さくひん', u'sakuhin'),
    # 89. 時代
    (u'じだい', u'jidai'),
    # 90. これ
    (u'これ', u'kore'),
    # 91. 位
    (u'い', u'i'),
    # 92. 版
    (u'はん', u'han'),
    # 93. 数
    (u'しばしば', u'shibashiba'),
    # 94. 賞
    (u'しょう', u'shō'),
    # 95. 本
    (u'もと', u'moto'),
    # 96. 型
    (u'かた', u'kata'),
    # 97. 州
    (u'しゅう', u'shū'),
    # 98. 分
    (u'ふん', u'fun'),
    # 99. 上
    (u'うえ', u'ue'),
    # 100. 話
    (u'わ', u'wa'),
    # 101. 元
    (u'げん', u'gen'),
    # 102. 登場
    (u'とう|じょう', u'tōjō'),
    # 103. 間
    (u'あいだ', u'aida'),
    # 104. 社
    (u'しゃ', u'sha'),
    # 105. 局
    (u'きょく', u'kyoku'),
    # 106. 項目
    (u'こう|もく', u'kōmoku'),
    # 107. 出演
    (u'しゅつえん', u'shutsuen'),
    # 108. 平成
    (u'へいせい', u'heisei'),
    # 109. 地
    (u'じ', u'ji'),
    # 110. 目
    (u'もく', u'moku'),
    # 111. 道
    (u'どう', u'dō'),
    # 112. 曲
    (u'まが', u'maga'),
    # 113. 使用
    (u'し|よう', u'shiyō'),
    # 114. 他
    (u'た', u'ta'),
    # 115. 持つ
    (u'もつ', u'motsu'),
    # 116. 場合
    (u'ばあい', u'bāi'),
    # 117. 性
    (u'しょう', u'shō'),
    # 118. 監督
    (u'かんとく', u'kantoku'),
    # 119. 軍
    (u'ぐん', u'gun'),
    # 120. 発売
    (u'はつばい', u'hatsubai'),
    # 121. 選手
    (u'せんしゅ', u'senshu'),
    # 122. 新
    (u'しん', u'shin'),
    # 123. 大学
    (u'だいがく', u'daigaku'),
    # 124. 戦
    (u'せん', u'sen'),
    # 125. ば
    (u'ば', u'ba'),
    # 126. 代表
    (u'だい|ひょう', u'daihyō'),
    # 127. 所
    (u'しょ', u'sho'),
    # 128. 活動
    (u'かつどう', u'katsudō'),
    # 129. 研究
    (u'けんきゅう', u'kenkyū'),
    # 130. 呼ぶ
    (u'よぶ', u'yobu'),
    # 131. 機
    (u'き', u'ki'),
    # 132. 系
    (u'けい', u'kei'),
    # 133. う
    (u'う', u'u'),
    # 134. 内
    (u'ない', u'nai'),
    # 135. 情報
    (u'じょう|ほう', u'jōhō'),
    # 136. さ
    (u'さ', u'sa'),
    # 137. 多い
    (u'おおい', u'ōi'),
    # 138. について
    (u'について', u'nitsuite'),
    # 139. 次
    (u'じ', u'ji'),
    # 140. 鉄道
    (u'てつどう', u'tetsudō'),
    # 141. 脚注
    (u'きゃくちゅう', u'kyakuchū'),
    # 142. 等
    (u'とう', u'tō'),
    # 143. において
    (u'において', u'nioite'),
    # 144. 時間
    (u'じかん', u'jikan'),
    # 145. 主
    (u'しゅ', u'shu'),
    # 146. チーム
    (u'チーム', u'chīmu'),
    # 147. それ
    (u'それ', u'sore'),
    # 148. 初
    (u'はつ', u'hatsu'),
    # 149. のみ
    (u'のみ', u'nomi'),
    # 150. 万
    (u'ばん', u'ban'),
    # 151. シリーズ
    (u'シリーズ', u'shirīzu'),
    # 152. その後
    (u'そのご', u'sonogo'),
    # 153. 所属
    (u'しょぞく', u'shozoku'),
    # 154. 役
    (u'えき', u'eki'),
    # 155. 受ける
    (u'うける', u'ukeru'),
    # 156. 科
    (u'か', u'ka'),
    # 157. 作曲
    (u'さっきょく', u'sakkyoku'),
    # 158. 出身
    (u'しゅっしん', u'shusshin'),
    # 159. 高等
    (u'こう|とう', u'kōtō'),
    # 160. 開始
    (u'かいし', u'kaishi'),
    # 161. 場
    (u'じょう', u'jō'),
    # 162. 公式
    (u'こう|しき', u'kōshiki'),
    # 163. 学
    (u'がく', u'gaku'),
    # 164. しかし
    (u'しかし', u'shikashi'),
    # 165. アメリカ
    (u'アメリカ', u'amerika'),
    # 166. 存在
    (u'そんざい', u'sonzai'),
    # 167. くる
    (u'くる', u'kuru'),
    # 168. 作
    (u'さく', u'saku'),
    # 169. 車
    (u'くるま', u'kuruma'),
    # 170. 大会
    (u'たいかい', u'taikai'),
    # 171. 人物
    (u'じんぶつ', u'jinbutsu'),
    # 172. たち
    (u'たち', u'tachi'),
    # 173. 形
    (u'かた', u'kata'),
    # 174. ゲーム
    (u'ゲーム', u'gēmu'),
    # 175. 一覧
    (u'いちらん', u'ichiran'),
    # 176. 語
    (u'ご', u'go'),
    # 177. バス
    (u'バス', u'basu'),
    # 178. 株式会社
    (u'かぶしきがいしゃ', u'kabushikigaisha'),
    # 179. 法
    (u'ほう', u'hō'),
    # 180. 歳
    (u'さい', u'sai'),
    # 181. 大阪
    (u'おお|さか', u'ōsaka'),
    # 182. いう
    (u'いう', u'iu'),
    # 183. 音楽
    (u'おんがく', u'ongaku'),
    # 184. お
    (u'お', u'o'),
    # 185. 同
    (u'どう', u'dō'),
    # 186. 当時
    (u'とう|じ', u'tōji'),
    # 187. 事業
    (u'じ|ぎょう', u'jigyō'),
    # 188. 歴史
    (u'れきし', u'rekishi'),
    # 189. 可能
    (u'か|のう', u'kanō'),
    # 190. 教育
    (u'きょう|いく', u'kyōiku'),
    # 191. 式
    (u'しき', u'shiki'),
    # 192. 一部
    (u'いちぶ', u'ichibu'),
    # 193. 見る
    (u'みる', u'miru'),
    # 194. 約
    (u'やく', u'yaku'),
    # 195. 小学校
    (u'しょう|がっこう', u'shōgakkō'),
    # 196. 出場
    (u'しゅつ|じょう', u'shutsujō'),
    # 197. ドラマ
    (u'ドラマ', u'dorama'),
    # 198. 全
    (u'ぜん', u'zen'),
    # 199. 国際
    (u'こくさい', u'kokusai'),
    # 200. 地域
    (u'ちいき', u'chiiki'),
    # 201. 開発
    (u'かいはつ', u'kaihatsu'),
    # 202. 用
    (u'よう', u'yō'),
    # 203. つ
    (u'つ', u'tsu'),
    # 204. 関係
    (u'かんけい', u'kankei'),
    # 205. 収録
    (u'しゅうろく', u'shūroku'),
    # 206. 事
    (u'ごと', u'goto'),
    # 207. 明治
    (u'めいじ', u'meiji'),
    # 208. 長
    (u'つかさ', u'tsukasa'),
    # 209. 期
    (u'き', u'ki'),
    # 210. 彼
    (u'あれ', u'are'),
    # 211. 際
    (u'きわ', u'kiwa'),
    # 212. ら
    (u'ら', u'ra'),
    # 213. 概要
    (u'がい|よう', u'gaiyō'),
    # 214. 使う
    (u'つかう', u'tsukau'),
    # 215. 旧
    (u'きゅう', u'kyū'),
    # 216. アルバム
    (u'アルバム', u'arubamu'),
    # 217. アニメ
    (u'アニメ', u'anime'),
    # 218. 声
    (u'こえ', u'koe'),
    # 219. および
    (u'および', u'oyobi'),
    # 220. 会社
    (u'かいしゃ', u'kaisha'),
    # 221. しまう
    (u'しまう', u'shimau'),
    # 222. 円
    (u'えん', u'en'),
    # 223. 優勝
    (u'ゆう|しょう', u'yūshō'),
    # 224. サイト
    (u'サイト', u'saito'),
    # 225. なお
    (u'なお', u'nao'),
    # 226. における
    (u'における', u'niokeru'),
    # 227. 南
    (u'みなみ', u'minami'),
    # 228. 設置
    (u'せっち', u'setchi'),
    # 229. 十
    (u'シー', u'shī'),
    # 230. 開催
    (u'かいさい', u'kaisai'),
    # 231. 下
    (u'か', u'ka'),
    # 232. 作詞
    (u'さくし', u'sakushi'),
    # 233. 北
    (u'きた', u'kita'),
    # 234. 度
    (u'たび', u'tabi'),
    # 235. 巻
    (u'かん', u'kan'),
    # 236. 世
    (u'せい', u'sei'),
    # 237. 力
    (u'ちから', u'chikara'),
    # 238. 言う
    (u'いう', u'iu'),
    # 239. 出版
    (u'しゅっぱん', u'shuppan'),
    # 240. 知る
    (u'しる', u'shiru'),
    # 241. 王
    (u'おう', u'ō'),
    # 242. 変更
    (u'へん|こう', u'henkō'),
    # 243. 担当
    (u'たん|とう', u'tantō'),
    # 244. たり
    (u'たり', u'tari'),
    # 245. 廃止
    (u'はいし', u'haishi'),
    # 246. 委員
    (u'いいん', u'iin'),
    # 247. 色
    (u'いろ', u'iro'),
    # 248. 都市
    (u'とし', u'toshi'),
    # 249. 高
    (u'こう', u'kō'),
    # 250. 参加
    (u'さんか', u'sanka'),
    # 251. 利用
    (u'り|よう', u'riyō'),
    # 252. 製作
    (u'せいさく', u'seisaku'),
    # 253. 位置
    (u'いち', u'ichi'),
    # 254. 店
    (u'たな', u'tana'),
    # 255. 事件
    (u'じけん', u'jiken'),
    # 256. 中央
    (u'ちゅう|おう', u'chūō'),
    # 257. 名称
    (u'めい|しょう', u'meishō'),
    # 258. 氏
    (u'うじ', u'uji'),
    # 259. 市立
    (u'しりつ', u'shiritsu'),
    # 260. 一般
    (u'いっぱん', u'ippan'),
    # 261. にて
    (u'にて', u'nite'),
    # 262. だけ
    (u'だけ', u'dake'),
    # 263. 級
    (u'きゅう', u'kyū'),
    # 264. 都
    (u'と', u'to'),
    # 265. 以降
    (u'い|こう', u'ikō'),
    # 266. 東
    (u'ひがし', u'higashi'),
    # 267. 制作
    (u'せいさく', u'seisaku'),
    # 268. 野球
    (u'やきゅう', u'yakyū'),
    # 269. 設立
    (u'せつりつ', u'setsuritsu'),
    # 270. センター
    (u'センター', u'sentā'),
    # 271. 試合
    (u'しあい', u'shiai'),
    # 272. ん
    (u'ん', u'n'),
    # 273. 番
    (u'ばん', u'ban'),
    # 274. 高い
    (u'たかい', u'takai'),
    # 275. 中心
    (u'なかご', u'nakago'),
    # 276. 番号
    (u'ばんごう', u'bangō'),
    # 277. 年度
    (u'ねんど', u'nendo'),
    # 278. 年代
    (u'ねんだい', u'nendai'),
    # 279. 機関
    (u'きかん', u'kikan'),
    # 280. 発表
    (u'はっ|ぴょう', u'happyō'),
    # 281. その他
    (u'そのほか', u'sonohoka'),
    # 282. 以上
    (u'い|じょう', u'ijō'),
    # 283. 同じ
    (u'おなじ', u'onaji'),
    # 284. 現
    (u'げん', u'gen'),
    # 285. 問題
    (u'もんだい', u'mondai'),
    # 286. 代
    (u'よ', u'yo'),
    # 287. ドイツ
    (u'ドイツ', u'doitsu'),
    # 288. いく
    (u'いく', u'iku'),
    # 289. 編
    (u'へん', u'hen'),
    # 290. 参考
    (u'さん|こう', u'sankō'),
    # 291. 子
    (u'こう', u'kō'),
    # 292. 及び
    (u'および', u'oyobi'),
    # 293. 道路
    (u'どうろ', u'dōro'),
    # 294. 郵便
    (u'ゆうびん', u'yūbin'),
    # 295. 地方
    (u'じかた', u'jikata'),
    # 296. 用いる
    (u'もちいる', u'mochiiru'),
    # 297. 社会
    (u'しゃかい', u'shakai'),
    # 298. 記録
    (u'きろく', u'kiroku'),
    # 299. 多く
    (u'おおく', u'ōku'),
    # 300. リーグ
    (u'リーグ', u'rīgu'),
    # 301. 種
    (u'くさ', u'kusa'),
    # 302. 中学校
    (u'ちゅう|がっこう', u'chūgakkō'),
    # 303. 金
    (u'おうごん', u'ōgon'),
    # 304. 路線
    (u'ろせん', u'rosen'),
    # 305. 点
    (u'ちょぼ', u'chobo'),
    # 306. 中国
    (u'ちゅうごく', u'chūgoku'),
    # 307. 総
    (u'そう', u'sō'),
    # 308. 以下
    (u'いか', u'ika'),
    # 309. 体
    (u'たい', u'tai'),
    # 310. プロ
    (u'プロ', u'puro'),
    # 311. 島
    (u'とう', u'tō'),
    # 312. 施設
    (u'しせつ', u'shisetsu'),
    # 313. 編曲
    (u'へんきょく', u'henkyoku'),
    # 314. 人口
    (u'じん|こう', u'jinkō'),
    # 315. 丁目
    (u'ちょう|め', u'chōme'),
    # 316. 文献
    (u'ぶんけん', u'bunken'),
    # 317. 文化
    (u'ぶんか', u'bunka'),
    # 318. 別
    (u'べつ', u'betsu'),
    # 319. 同年
    (u'どうねん', u'dōnen'),
    # 320. 側
    (u'がわ', u'gawa'),
    # 321. 攻撃
    (u'こう|げき', u'kōgeki'),
    # 322. 女性
    (u'じょせい', u'josei'),
    # 323. 西
    (u'せい', u'sei'),
    # 324. 京都
    (u'きょう|と', u'kyōto'),
    # 325. ラジオ
    (u'ラジオ', u'rajio'),
    # 326. 入る
    (u'いる', u'iru'),
    # 327. さらに
    (u'さらに', u'sarani'),
    # 328. 交通
    (u'こう|つう', u'kōtsū'),
    # 329. 頃
    (u'けい', u'kei'),
    # 330. サッカー
    (u'サッカー', u'sakkā'),
    # 331. シングル
    (u'シングル', u'shinguru'),
    # 332. 面
    (u'おもて', u'omote'),
    # 333. クラブ
    (u'クラブ', u'kurabu'),
    # 334. 四
    (u'スー', u'sū'),
    # 335. 各
    (u'かく', u'kaku'),
    # 336. フランス
    (u'フランス', u'furansu'),
    # 337. 記念
    (u'きねん', u'kinen'),
    # 338. 名前
    (u'なまえ', u'namae'),
    # 339. 所在地
    (u'しょざいち', u'shozaichi'),
    # 340. 自分
    (u'じぶん', u'jibun'),
    # 341. 手
    (u'て', u'te'),
    # 342. ほか
    (u'ほか', u'hoka'),
    # 343. 物
    (u'ぶつ', u'butsu'),
    # 344. 務める
    (u'つとめる', u'tsutomeru'),
    # 345. 川
    (u'かわ', u'kawa'),
    # 346. 選手権
    (u'せんしゅけん', u'senshuken'),
    # 347. 協会
    (u'きょう|かい', u'kyōkai'),
    # 348. 最終
    (u'さいしゅう', u'saishū'),
    # 349. 含む
    (u'ふくむ', u'fukumu'),
    # 350. 城
    (u'き', u'ki'),
    # 351. イギリス
    (u'イギリス', u'igirisu'),
    # 352. キャラクター
    (u'キャラクター', u'kyarakutā'),
    # 353. 内容
    (u'ない|よう', u'naiyō'),
    # 354. 地区
    (u'ちく', u'chiku'),
    # 355. 必要
    (u'ひつ|よう', u'hitsuyō'),
    # 356. 両
    (u'もろ', u'moro'),
    # 357. 終了
    (u'しゅう|りょう', u'shūryō'),
    # 358. 総合
    (u'そう|ごう', u'sōgō'),
    # 359. 計画
    (u'けいかく', u'keikaku'),
    # 360. ファイル
    (u'ファイル', u'fairu'),
    # 361. 女
    (u'め', u'me'),
    # 362. 制
    (u'せい', u'sei'),
    # 363. 公開
    (u'こう|かい', u'kōkai'),
    # 364. 販売
    (u'はんばい', u'hanbai'),
    # 365. 神
    (u'かみ', u'kami'),
    # 366. 世紀
    (u'せいき', u'seiki'),
    # 367. 政治
    (u'せいじ', u'seiji'),
    # 368. 表記
    (u'ひょう|き', u'hyōki'),
    # 369. 艦
    (u'かん', u'kan'),
    # 370. に対して
    (u'にたいして', u'nitaishite'),
    # 371. 史
    (u'し', u'shi'),
    # 372. 特別
    (u'とくべつ', u'tokubetsu'),
    # 373. 技術
    (u'ぎじゅつ', u'gijutsu'),
    # 374. 生
    (u'うぶ', u'ubu'),
    # 375. 漫画
    (u'まんが', u'manga'),
    # 376. 館
    (u'かん', u'kan'),
    # 377. 員
    (u'いん', u'in'),
    # 378. ながら
    (u'ながら', u'nagara'),
    # 379. 隊
    (u'たい', u'tai'),
    # 380. シーズン
    (u'シーズン', u'shīzun'),
    # 381. 高校
    (u'こう|こう', u'kōkō'),
    # 382. 考える
    (u'かんがえる', u'kangaeru'),
    # 383. 全国
    (u'ぜんこく', u'zenkoku'),
    # 384. 結果
    (u'けっか', u'kekka'),
    # 385. 説明
    (u'せつめい', u'setsumei'),
    # 386. 選挙
    (u'せんきょ', u'senkyo'),
    # 387. 卒業
    (u'そつ|ぎょう', u'sotsugyō'),
    # 388. 歌
    (u'うた', u'uta'),
    # 389. 経済
    (u'けいざい', u'keizai'),
    # 390. 英語
    (u'えいご', u'eigo'),
    # 391. 競技
    (u'きょう|ぎ', u'kyōgi'),
    # 392. 勝
    (u'しょう', u'shō'),
    # 393. 人間
    (u'じんかん', u'jinkan'),
    # 394. 台
    (u'うてな', u'utena'),
    # 395. でも
    (u'でも', u'demo'),
    # 396. グループ
    (u'グループ', u'gurūpu'),
    # 397. 五
    (u'ウー', u'ū'),
    # 398. 女子
    (u'じょし', u'joshi'),
    # 399. 男
    (u'おとこ', u'otoko'),
    # 400. 営業
    (u'えい|ぎょう', u'eigyō'),
    # 401. 国道
    (u'こくどう', u'kokudō'),
    # 402. 劇場
    (u'げき|じょう', u'gekijō'),
    # 403. 父
    (u'ちち', u'chichi'),
    # 404. 科学
    (u'かがく', u'kagaku'),
    # 405. 戦争
    (u'せん|そう', u'sensō'),
    # 406. 自身
    (u'じしん', u'jishin'),
    # 407. とき
    (u'とき', u'toki'),
    # 408. 枠
    (u'わく', u'waku'),
    # 409. 以外
    (u'いがい', u'igai'),
    # 410. 同様
    (u'どう|よう', u'dōyō'),
    # 411. 府
    (u'ふ', u'fu'),
    # 412. 指定
    (u'してい', u'shitei'),
    # 413. 得る
    (u'うる', u'uru'),
    # 414. モデル
    (u'モデル', u'moderu'),
    # 415. 車両
    (u'しゃ|りょう', u'sharyō'),
    # 416. に関する
    (u'にかんする', u'nikansuru'),
    # 417. うち
    (u'うち', u'uchi'),
    # 418. 教授
    (u'きょう|じゅ', u'kyōju'),
    # 419. 馬
    (u'うま', u'uma'),
    # 420. 管理
    (u'かんり', u'kanri'),
    # 421. 北海道
    (u'ほっかいどう', u'hokkaidō'),
    # 422. 再
    (u'さい', u'sai'),
    # 423. と共に
    (u'とともに', u'totomoni'),
    # 424. 星
    (u'せい', u'sei'),
    # 425. 構成
    (u'こう|せい', u'kōsei'),
    # 426. 枚
    (u'びら', u'bira'),
    # 427. 列車
    (u'れっしゃ', u'ressha'),
    # 428. 参照
    (u'さん|しょう', u'sanshō'),
    # 429. 文庫
    (u'ぶんこ', u'bunko'),
    # 430. 当初
    (u'とう|しょ', u'tōsho'),
    # 431. 花
    (u'はな', u'hana'),
    # 432. メンバー
    (u'メンバー', u'menbā'),
    # 433. 作る
    (u'つくる', u'tsukuru'),
    # 434. 影響
    (u'えい|きょう', u'eikyō'),
    # 435. たい
    (u'たい', u'tai'),
    # 436. 異なる
    (u'ことなる', u'kotonaru'),
    # 437. 受賞
    (u'じゅ|しょう', u'jushō'),
    # 438. 部分
    (u'ぶぶん', u'bubun'),
    # 439. 秒
    (u'びょう', u'byō'),
    # 440. サイズ
    (u'サイズ', u'saizu'),
    # 441. 建設
    (u'けんせつ', u'kensetsu'),
    # 442. 期間
    (u'きかん', u'kikan'),
    # 443. 伴う
    (u'ともなう', u'tomonau'),
    # 444. システム
    (u'システム', u'shisutemu'),
    # 445. 山
    (u'さん', u'san'),
    # 446. 大きい
    (u'おおきい', u'ōkii'),
    # 447. 自動車
    (u'じどうしゃ', u'jidōsha'),
    # 448. 室
    (u'しつ', u'shitsu'),
    # 449. 出る
    (u'でる', u'deru'),
    # 450. 特に
    (u'とくに', u'tokuni'),
    # 451. 合併
    (u'がっぺい', u'gappei'),
    # 452. 娘
    (u'じょう', u'jō'),
    # 453. とともに
    (u'とともに', u'totomoni'),
    # 454. 最後
    (u'さいご', u'saigo'),
    # 455. ので
    (u'ので', u'node'),
    # 456. 政府
    (u'せいふ', u'seifu'),
    # 457. 戦闘
    (u'せん|とう', u'sentō'),
    # 458. 写真
    (u'しゃしん', u'shashin'),
    # 459. 団
    (u'だん', u'dan'),
    # 460. 達
    (u'たち', u'tachi'),
    # 461. 製造
    (u'せいぞう', u'seizō'),
    # 462. 小
    (u'さ', u'sa'),
    # 463. 議員
    (u'ぎいん', u'giin'),
    # 464. 最初
    (u'さいしょ', u'saisho'),
    # 465. 組織
    (u'そしき', u'soshiki'),
    # 466. タイトル
    (u'タイトル', u'taitoru'),
    # 467. 構造
    (u'こう|ぞう', u'kōzō'),
    # 468. ほど
    (u'ほど', u'hodo'),
    # 469. 獲得
    (u'かくとく', u'kakutoku'),
    # 470. 組
    (u'くみ', u'kumi'),
    # 471. かつて
    (u'かつて', u'katsute'),
    # 472. 水
    (u'すい', u'sui'),
    # 473. 校
    (u'こう', u'kō'),
    # 474. ただし
    (u'ただし', u'tadashi'),
    # 475. 県立
    (u'けんりつ', u'kenritsu'),
    # 476. 撮影
    (u'さつえい', u'satsuei'),
    # 477. 場所
    (u'ばしょ', u'basho'),
    # 478. 企画
    (u'きかく', u'kikaku'),
    # 479. 官
    (u'かん', u'kan'),
    # 480. デビュー
    (u'デビュー', u'debyū'),
    # 481. 派
    (u'は', u'ha'),
    # 482. 小説
    (u'しょう|せつ', u'shōsetsu'),
    # 483. 企業
    (u'き|ぎょう', u'kigyō'),
    # 484. 与える
    (u'あたえる', u'ataeru'),
    # 485. 通り
    (u'とおり', u'tōri'),
    # 486. 広島
    (u'ひろしま', u'hiroshima'),
    # 487. 権
    (u'けん', u'ken'),
    # 488. 強い
    (u'こわい', u'kowai'),
    # 489. 設定
    (u'せってい', u'settei'),
    # 490. 状態
    (u'じょう|たい', u'jōtai'),
    # 491. 愛
    (u'あい', u'ai'),
    # 492. 橋
    (u'きょう', u'kyō'),
    # 493. 条
    (u'すじ', u'suji'),
    # 494. 一つ
    (u'ひとつ', u'hitotsu'),
    # 495. 発生
    (u'はっせい', u'hassei'),
    # 496. アメリカ合衆国
    (u'アメリカがっしゅうこく', u'amerikagasshūkoku'),
    # 497. テーマ
    (u'テーマ', u'tēma'),
    # 498. 主義
    (u'しゅぎ', u'shugi'),
    # 499. そして
    (u'そして', u'soshite'),
    # 500. 年間
    (u'ねんかん', u'nenkan'),
    # 501. よる
    (u'よる', u'yoru'),
    # 502. 方
    (u'へ', u'he'),
    # 503. 物語
    (u'ものがたり', u'monogatari'),
    # 504. 機能
    (u'き|のう', u'kinō'),
    # 505. 最高
    (u'さい|こう', u'saikō'),
    # 506. 航空
    (u'こう|くう', u'kōkū'),
    # 507. 成績
    (u'せいせき', u'seiseki'),
    # 508. 光
    (u'ひかり', u'hikari'),
    # 509. 福岡
    (u'ふくおか', u'fukuoka'),
    # 510. 公園
    (u'こう|えん', u'kōen'),
    # 511. 決定
    (u'けってい', u'kettei'),
    # 512. 海軍
    (u'かいぐん', u'kaigun'),
    # 513. それぞれ
    (u'それぞれ', u'sorezore'),
    # 514. 就任
    (u'しゅうにん', u'shūnin'),
    # 515. 法人
    (u'ほう|じん', u'hōjin'),
    # 516. 神社
    (u'じんじゃ', u'jinja'),
    # 517. 描く
    (u'えがく', u'egaku'),
    # 518. デザイン
    (u'デザイン', u'dezain'),
    # 519. 能力
    (u'のう|りょく', u'nōryoku'),
    # 520. 意味
    (u'いみ', u'imi'),
    # 521. 生活
    (u'せいかつ', u'seikatsu'),
    # 522. フジテレビ
    (u'フジテレビ', u'fujiterebi'),
    # 523. または
    (u'または', u'mataha'),
    # 524. 主要
    (u'しゅ|よう', u'shuyō'),
    # 525. 専門
    (u'せんもん', u'senmon'),
    # 526. 書
    (u'しょ', u'sho'),
    # 527. 一方
    (u'いっぽう', u'ippō'),
    # 528. 編集
    (u'へんしゅう', u'henshū'),
    # 529. 最大
    (u'さいだい', u'saidai'),
    # 530. 原作
    (u'げんさく', u'gensaku'),
    # 531. 名古屋
    (u'なごや', u'nagoya'),
    # 532. 脚本
    (u'きゃくほん', u'kyakuhon'),
    # 533. 率
    (u'りつ', u'ritsu'),
    # 534. 対応
    (u'たい|おう', u'taiō'),
    # 535. 院
    (u'いん', u'in'),
    # 536. 面積
    (u'めんせき', u'menseki'),
    # 537. 運行
    (u'うん|こう', u'unkō'),
    # 538. 通常
    (u'つう|じょう', u'tsūjō'),
    # 539. 彼女
    (u'かのじょ', u'kanojo'),
    # 540. 八
    (u'パー', u'pā'),
    # 541. これら
    (u'これら', u'korera'),
    # 542. 種類
    (u'しゅるい', u'shurui'),
    # 543. き
    (u'き', u'ki'),
    # 544. 対
    (u'たい', u'tai'),
    # 545. とも
    (u'とも', u'tomo'),
    # 546. 発行
    (u'はっ|こう', u'hakkō'),
    # 547. 続ける
    (u'つづける', u'tsuzukeru'),
    # 548. 過去
    (u'かこ', u'kako'),
    # 549. 身長
    (u'しん|ちょう', u'shinchō'),
    # 550. ま
    (u'ま', u'ma'),
    # 551. ます
    (u'ます', u'masu'),
    # 552. 出典
    (u'しゅってん', u'shutten'),
    # 553. 病院
    (u'びょう|いん', u'byōin'),
    # 554. 生産
    (u'せいさん', u'seisan'),
    # 555. 宇宙
    (u'うちゅう', u'uchū'),
    # 556. 何
    (u'なに', u'nani'),
    # 557. 採用
    (u'さい|よう', u'saiyō'),
    # 558. 千
    (u'せん', u'sen'),
    # 559. 基本
    (u'きほん', u'kihon'),
    # 560. 生まれる
    (u'うまれる', u'umareru'),
    # 561. 全て
    (u'すべて', u'subete'),
    # 562. 風
    (u'ふり', u'furi'),
    # 563. ダム
    (u'ダム', u'damu'),
    # 564. 警察
    (u'けいさつ', u'keisatsu'),
    # 565. さん
    (u'さん', u'san'),
    # 566. 指揮
    (u'しき', u'shiki'),
    # 567. 六
    (u'リュー', u'ryū'),
    # 568. スポーツ
    (u'スポーツ', u'supōtsu'),
    # 569. 置く
    (u'おく', u'oku'),
    # 570. 音
    (u'おと', u'oto'),
    # 571. 超
    (u'ちょう', u'chō'),
    # 572. 編成
    (u'へんせい', u'hensei'),
    # 573. 字
    (u'あざ', u'aza'),
    # 574. 朝
    (u'あさ', u'asa'),
    # 575. 搭載
    (u'とう|さい', u'tōsai'),
    # 576. 出す
    (u'だす', u'dasu'),
    # 577. 思う
    (u'おもう', u'omō'),
    # 578. 海
    (u'うみ', u'umi'),
    # 579. 百
    (u'ひゃく', u'hyaku'),
    # 580. 運転
    (u'うんてん', u'unten'),
    # 581. 周辺
    (u'しゅうへん', u'shūhen'),
    # 582. 調査
    (u'ちょう|さ', u'chōsa'),
    # 583. みる
    (u'みる', u'miru'),
    # 584. 連続
    (u'れんぞく', u'renzoku'),
    # 585. 億
    (u'おく', u'oku'),
    # 586. 母
    (u'はは', u'haha'),
    # 587. 特徴
    (u'とく|ちょう', u'tokuchō'),
    # 588. 続く
    (u'つづく', u'tsuzuku'),
    # 589. 少年
    (u'しょう|ねん', u'shōnen'),
    # 590. 独立
    (u'どくりつ', u'dokuritsu'),
    # 591. 本社
    (u'ほんしゃ', u'honsha'),
    # 592. 開業
    (u'かい|ぎょう', u'kaigyō'),
    # 593. 行く
    (u'いく', u'iku'),
    # 594. ものの
    (u'ものの', u'monono'),
    # 595. 相手
    (u'あいて', u'aite'),
    # 596. 戦い
    (u'たたかい', u'tatakai'),
    # 597. 心
    (u'こころ', u'kokoro'),
    # 598. 始める
    (u'はじめる', u'hajimeru'),
    # 599. サービス
    (u'サービス', u'sābisu'),
    # 600. 目的
    (u'もくてき', u'mokuteki'),
    # 601. ロシア
    (u'ロシア', u'roshia'),
    # 602. 実施
    (u'じっし', u'jisshi'),
    # 603. に対する
    (u'にたいする', u'nitaisuru'),
    # 604. 例
    (u'れい', u'rei'),
    # 605. 街
    (u'がい', u'gai'),
    # 606. 基礎
    (u'きそ', u'kiso'),
    # 607. 省
    (u'しょう', u'shō'),
    # 608. 藩
    (u'はん', u'han'),
    # 609. 事務所
    (u'じむしょ', u'jimusho'),
    # 610. コード
    (u'コード', u'kōdo'),
    # 611. 部隊
    (u'ぶたい', u'butai'),
    # 612. 設計
    (u'せっけい', u'sekkei'),
    # 613. 姿
    (u'すがた', u'sugata'),
    # 614. 妻
    (u'さい', u'sai'),
    # 615. 横浜
    (u'よこはま', u'yokohama'),
    # 616. 紹介
    (u'しょう|かい', u'shōkai'),
    # 617. ところ
    (u'ところ', u'tokoro'),
    # 618. 集
    (u'しゅう', u'shū'),
    # 619. 高速
    (u'こう|そく', u'kōsoku'),
    # 620. 行政
    (u'ぎょう|せい', u'gyōsei'),
    # 621. 代目
    (u'だいめ', u'daime'),
    # 622. 分類
    (u'ぶんるい', u'bunrui'),
    # 623. 森
    (u'もり', u'mori'),
    # 624. 得点
    (u'とくてん', u'tokuten'),
    # 625. 右
    (u'みぎ', u'migi'),
    # 626. 理由
    (u'りゆう', u'riyū'),
    # 627. マン
    (u'マン', u'man'),
    # 628. 帝国
    (u'ていこく', u'teikoku'),
    # 629. 不明
    (u'ふめい', u'fumei'),
    # 630. 運動
    (u'うんどう', u'undō'),
    # 631. 副
    (u'ふく', u'fuku'),
    # 632. 勝利
    (u'しょう|り', u'shōri'),
    # 633. 江戸
    (u'えど', u'edo'),
    # 634. 最も
    (u'もっとも', u'mottomo'),
    # 635. 年月日
    (u'ねんがっぴ', u'nengappi'),
    # 636. 章
    (u'しょう', u'shō'),
    # 637. 建築
    (u'けんちく', u'kenchiku'),
    # 638. じ
    (u'じ', u'ji'),
    # 639. 和書
    (u'わしょ', u'washo'),
    # 640. 経営
    (u'けいえい', u'keiei'),
    # 641. 新潟
    (u'にいがた', u'niigata'),
    # 642. 没
    (u'ぼつ', u'botsu'),
    # 643. 長い
    (u'ながい', u'nagai'),
    # 644. 示す
    (u'しめす', u'shimesu'),
    # 645. 俳優
    (u'はいゆう', u'haiyū'),
    # 646. エンジン
    (u'エンジン', u'enjin'),
    # 647. ニュース
    (u'ニュース', u'nyūsu'),
    # 648. 発見
    (u'はっけん', u'hakken'),
    # 649. データ
    (u'データ', u'dēta'),
    # 650. 夏
    (u'か', u'ka'),
    # 651. ホーム
    (u'ホーム', u'hōmu'),
    # 652. 群
    (u'ぐん', u'gun'),
    # 653. 無い
    (u'ない', u'nai'),
    # 654. 以前
    (u'いぜん', u'izen'),
    # 655. 備考
    (u'び|こう', u'bikō'),
    # 656. よ
    (u'よ', u'yo'),
    # 657. 正
    (u'しょう', u'shō'),
    # 658. 契約
    (u'けいやく', u'keiyaku'),
    # 659. 本名
    (u'ほん|みょう', u'honmyō'),
    # 660. 文字
    (u'もじ', u'moji'),
    # 661. 時点
    (u'じてん', u'jiten'),
    # 662. 運営
    (u'うんえい', u'un\'ei'),
    # 663. 初めて
    (u'はじめて', u'hajimete'),
    # 664. イタリア
    (u'イタリア', u'itaria'),
    # 665. 提供
    (u'てい|きょう', u'teikyō'),
    # 666. 大正
    (u'たい|しょう', u'taishō'),
    # 667. 書く
    (u'かく', u'kaku'),
    # 668. 国内
    (u'こくない', u'kokunai'),
    # 669. カード
    (u'カード', u'kādo'),
    # 670. 士
    (u'し', u'shi'),
    # 671. 連合
    (u'れんごう', u'rengō'),
    # 672. 表
    (u'おもて', u'omote'),
    # 673. 完成
    (u'かんせい', u'kansei'),
    # 674. 師
    (u'し', u'shi'),
    # 675. 活躍
    (u'かつやく', u'katsuyaku'),
    # 676. 米
    (u'こめ', u'kome'),
    # 677. 量
    (u'はか', u'haka'),
    # 678. スーパー
    (u'スーパー', u'sūpā'),
    # 679. 舞台
    (u'ぶたい', u'butai'),
    # 680. 予定
    (u'よてい', u'yotei'),
    # 681. 環境
    (u'かん|きょう', u'kankyō'),
    # 682. 韓国
    (u'かんこく', u'kankoku'),
    # 683. 団体
    (u'だんたい', u'dantai'),
    # 684. 家族
    (u'かぞく', u'kazoku'),
    # 685. 七
    (u'チー', u'chī'),
    # 686. のち
    (u'のち', u'nochi'),
    # 687. 自治体
    (u'じちたい', u'jichitai'),
    # 688. 祭
    (u'まつり', u'matsuri'),
    # 689. 実際
    (u'じっさい', u'jissai'),
    # 690. 重
    (u'おも', u'omo'),
    # 691. 社長
    (u'しゃ|ちょう', u'shachō'),
    # 692. 大きな
    (u'おおきな', u'ōkina'),
    # 693. 外
    (u'がい', u'gai'),
    # 694. 映像
    (u'えいぞう', u'eizō'),
    # 695. 日本語
    (u'にほんご', u'nihongo'),
    # 696. 学園
    (u'がくえん', u'gakuen'),
    # 697. 論
    (u'ろん', u'ron'),
    # 698. 技
    (u'わざ', u'waza'),
    # 699. 石
    (u'いし', u'ishi'),
    # 700. 時期
    (u'じき', u'jiki'),
    # 701. 現代
    (u'げんだい', u'gendai'),
    # 702. 文
    (u'ぶん', u'bun'),
    # 703. 族
    (u'ぞく', u'zoku'),
    # 704. べし
    (u'べし', u'beshi'),
    # 705. 協力
    (u'きょう|りょく', u'kyōryoku'),
    # 706. 千葉
    (u'ちば', u'chiba'),
    # 707. 解説
    (u'かいせつ', u'kaisetsu'),
    # 708. 船
    (u'ふね', u'fune'),
    # 709. 空港
    (u'くう|こう', u'kūkō'),
    # 710. 敵
    (u'てき', u'teki'),
    # 711. 共同
    (u'きょう|どう', u'kyōdō'),
    # 712. 自由
    (u'じゆう', u'jiyū'),
    # 713. 女優
    (u'じょゆう', u'joyū'),
    # 714. ライブ
    (u'ライブ', u'raibu'),
    # 715. リリース
    (u'リリース', u'rirīsu'),
    # 716. 階
    (u'かい', u'kai'),
    # 717. 港
    (u'こう', u'kō'),
    # 718. 研究所
    (u'けんきゅうしょ', u'kenkyūsho'),
    # 719. 演出
    (u'えんしゅつ', u'enshutsu'),
    # 720. 国家
    (u'こっか', u'kokka'),
    # 721. 方法
    (u'ほう|ほう', u'hōhō'),
    # 722. 学科
    (u'がっか', u'gakka'),
    # 723. 出来る
    (u'できる', u'dekiru'),
    # 724. 国立
    (u'こくりつ', u'kokuritsu'),
    # 725. ちゃん
    (u'ちゃん', u'chan'),
    # 726. 製
    (u'せい', u'sei'),
    # 727. 屋
    (u'や', u'ya'),
    # 728. ほとんど
    (u'ほとんど', u'hotondo'),
    # 729. 通信
    (u'つうしん', u'tsūshin'),
    # 730. 普通
    (u'ふつう', u'futsū'),
    # 731. コーナー
    (u'コーナー', u'kōnā'),
    # 732. 主演
    (u'しゅえん', u'shuen'),
    # 733. 加える
    (u'くわえる', u'kuwaeru'),
    # 734. といった
    (u'といった', u'toitta'),
    # 735. 完全
    (u'かんぜん', u'kanzen'),
    # 736. 初期
    (u'しょき', u'shoki'),
    # 737. 少女
    (u'しょう|じょ', u'shōjo'),
    # 738. 指導
    (u'しどう', u'shidō'),
    # 739. 重要
    (u'じゅう|よう', u'jūyō'),
    # 740. 仮
    (u'け', u'ke'),
    # 741. 認める
    (u'したためる', u'shitatameru'),
    # 742. 子供
    (u'こども', u'kodomo'),
    # 743. 愛知
    (u'あいち', u'aichi'),
    # 744. 工場
    (u'こう|じょう', u'kōjō'),
    # 745. 結婚
    (u'けっこん', u'kekkon'),
    # 746. しか
    (u'しか', u'shika'),
    # 747. 区間
    (u'くかん', u'kukan'),
    # 748. 対象
    (u'たい|しょう', u'taishō'),
    # 749. 経歴
    (u'けいれき', u'keireki'),
    # 750. 支援
    (u'しえん', u'shien'),
    # 751. 誕生
    (u'たん|じょう', u'tanjō'),
    # 752. 評価
    (u'ひょう|か', u'hyōka'),
    # 753. 訳
    (u'やく', u'yaku'),
    # 754. 公
    (u'きみ', u'kimi'),
    # 755. 新聞
    (u'しんぶん', u'shinbun'),
    # 756. 真
    (u'まな', u'mana'),
    # 757. プロデューサー
    (u'プロデューサー', u'purodūsā'),
    # 758. 電気
    (u'でんき', u'denki'),
    # 759. 中継
    (u'ちゅうけい', u'chūkei'),
    # 760. 改称
    (u'かい|しょう', u'kaishō'),
    # 761. 限定
    (u'げんてい', u'gentei'),
    # 762. 文学
    (u'ぶんがく', u'bungaku'),
    # 763. 大戦
    (u'たいせん', u'taisen'),
    # 764. 日本テレビ
    (u'にほんテレビ', u'nihonterebi'),
    # 765. テレビ朝日
    (u'テレビあさひ', u'terebiasahi'),
    # 766. 頭
    (u'どたま', u'dotama'),
    # 767. 夜
    (u'よる', u'yoru'),
    # 768. オリンピック
    (u'オリンピック', u'orinpikku'),
    # 769. 方式
    (u'ほう|しき', u'hōshiki'),
    # 770. 主人公
    (u'しゅ|じん|こう', u'shujinkō'),
    # 771. 血液
    (u'けつえき', u'ketsueki'),
    # 772. 圏
    (u'けん', u'ken'),
    # 773. 口
    (u'く', u'ku'),
    # 774. 取る
    (u'とる', u'toru'),
    # 775. ここ
    (u'ここ', u'koko'),
    # 776. 夢
    (u'ゆめ', u'yume'),
    # 777. 誌
    (u'し', u'shi'),
    # 778. 英
    (u'えい', u'ei'),
    # 779. 性格
    (u'せいかく', u'seikaku'),
    # 780. 形式
    (u'けいしき', u'keishiki'),
    # 781. 掲載
    (u'けいさい', u'keisai'),
    # 782. 行動
    (u'こう|どう', u'kōdō'),
    # 783. 表示
    (u'ひょう|じ', u'hyōji'),
    # 784. イベント
    (u'イベント', u'ibento'),
    # 785. 門
    (u'と', u'to'),
    # 786. 公演
    (u'こう|えん', u'kōen'),
    # 787. 会議
    (u'かいぎ', u'kaigi'),
    # 788. 先
    (u'せん', u'sen'),
    # 789. 果たす
    (u'はたす', u'hatasu'),
    # 790. 春
    (u'はる', u'haru'),
    # 791. 観光
    (u'かん|こう', u'kankō'),
    # 792. 学者
    (u'がくしゃ', u'gakusha'),
    # 793. 装置
    (u'そう|ち', u'sōchi'),
    # 794. 初代
    (u'しょだい', u'shodai'),
    # 795. 自ら
    (u'おのずから', u'onozukara'),
    # 796. 愛称
    (u'あい|しょう', u'aishō'),
    # 797. 陸軍
    (u'りくぐん', u'rikugun'),
    # 798. 言語
    (u'げんご', u'gengo'),
    # 799. 地球
    (u'ちきゅう', u'chikyū'),
    # 800. 作戦
    (u'さくせん', u'sakusen'),
    # 801. 成功
    (u'せい|こう', u'seikō'),
    # 802. 電車
    (u'でんしゃ', u'densha'),
    # 803. 移動
    (u'いどう', u'idō'),
    # 804. ご
    (u'ご', u'go'),
    # 805. 系列
    (u'けいれつ', u'keiretsu'),
    # 806. にかけて
    (u'にかけて', u'nikakete'),
    # 807. バンド
    (u'バンド', u'bando'),
    # 808. 為
    (u'す', u'su'),
    # 809. すべて
    (u'すべて', u'subete'),
    # 810. スペシャル
    (u'スペシャル', u'supesharu'),
    # 811. 郎
    (u'ろ', u'ro'),
    # 812. 男子
    (u'だんし', u'danshi'),
    # 813. 鈴木
    (u'すずき', u'suzuki'),
    # 814. 経る
    (u'へる', u'heru'),
    # 815. 方面
    (u'ほう|めん', u'hōmen'),
    # 816. 国民
    (u'こくみん', u'kokumin'),
    # 817. 除く
    (u'のぞく', u'nozoku'),
    # 818. り
    (u'り', u'ri'),
    # 819. 品
    (u'ひん', u'hin'),
    # 820. 向け
    (u'むけ', u'muke'),
    # 821. 様々
    (u'さまざま', u'samazama'),
    # 822. 由来
    (u'ゆらい', u'yurai'),
    # 823. 行
    (u'ぎょう', u'gyō'),
    # 824. 属
    (u'ぞく', u'zoku'),
    # 825. 距離
    (u'きょり', u'kyori'),
    # 826. 系統
    (u'けい|とう', u'keitō'),
    # 827. 基
    (u'き', u'ki'),
    # 828. 聖
    (u'せい', u'sei'),
    # 829. 今
    (u'いま', u'ima'),
    # 830. 山口
    (u'やまぐち', u'yamaguchi'),
    # 831. 同時に
    (u'どうじに', u'dōjini'),
    # 832. 状況
    (u'じょう|きょう', u'jōkyō'),
    # 833. ヨーロッパ
    (u'ヨーロッパ', u'yōroppa'),
    # 834. 多数
    (u'たすう', u'tasū'),
    # 835. 界
    (u'かい', u'kai'),
    # 836. 結ぶ
    (u'むすぶ', u'musubu'),
    # 837. 産業
    (u'さん|ぎょう', u'sangyō'),
    # 838. 雑誌
    (u'ざっし', u'zasshi'),
    # 839. 装備
    (u'そう|び', u'sōbi'),
    # 840. オリジナル
    (u'オリジナル', u'orijinaru'),
    # 841. 作家
    (u'さっか', u'sakka'),
    # 842. 非常
    (u'ひ|じょう', u'hijō'),
    # 843. 人気
    (u'じんき', u'jinki'),
    # 844. 岡山
    (u'おかやま', u'okayama'),
    # 845. 会長
    (u'かい|ちょう', u'kaichō'),
    # 846. 未
    (u'ひつじ', u'hitsuji'),
    # 847. 埼玉
    (u'さいたま', u'saitama'),
    # 848. 展開
    (u'てんかい', u'tenkai'),
    # 849. 導入
    (u'どうにゅう', u'dōnyū'),
    # 850. 統合
    (u'とう|ごう', u'tōgō'),
    # 851. 動物
    (u'どうぶつ', u'dōbutsu'),
    # 852. 始まる
    (u'はじまる', u'hajimaru'),
    # 853. 成立
    (u'せいりつ', u'seiritsu'),
    # 854. 寺
    (u'じ', u'ji'),
    # 855. 神戸
    (u'こう|べ', u'kōbe'),
    # 856. 国籍
    (u'こくせき', u'kokuseki'),
    # 857. 少ない
    (u'すくない', u'sukunai'),
    # 858. 長野
    (u'ながの', u'nagano'),
    # 859. 事項
    (u'じ|こう', u'jikō'),
    # 860. スタッフ
    (u'スタッフ', u'sutaffu'),
    # 861. 類
    (u'るい', u'rui'),
    # 862. 器
    (u'うつわ', u'utsuwa'),
    # 863. ガン
    (u'ガン', u'gan'),
    # 864. 教会
    (u'きょう|かい', u'kyōkai'),
    # 865. 競馬
    (u'くらべうま', u'kurabeuma'),
    # 866. 大統領
    (u'だい|とう|りょう', u'daitōryō'),
    # 867. 工業
    (u'こう|ぎょう', u'kōgyō'),
    # 868. かける
    (u'かける', u'kakeru'),
    # 869. 共和
    (u'きょう|わ', u'kyōwa'),
    # 870. 来る
    (u'くる', u'kuru'),
    # 871. 演奏
    (u'えん|そう', u'ensō'),
    # 872. 至る
    (u'いたる', u'itaru'),
    # 873. 部門
    (u'ぶもん', u'bumon'),
    # 874. 選ぶ
    (u'えらぶ', u'erabu'),
    # 875. 非
    (u'ひ', u'hi'),
    # 876. 整備
    (u'せいび', u'seibi'),
    # 877. 男性
    (u'だんせい', u'dansei'),
    # 878. 引退
    (u'いんたい', u'intai'),
    # 879. 自然
    (u'しぜん', u'shizen'),
    # 880. 党
    (u'とう', u'tō'),
    # 881. 再び
    (u'ふたたび', u'futatabi'),
    # 882. 個人
    (u'こじん', u'kojin'),
    # 883. に対し
    (u'にたいし', u'nitaishi'),
    # 884. 終わる
    (u'おわる', u'owaru'),
    # 885. 田中
    (u'たなか', u'tanaka'),
    # 886. 天
    (u'てん', u'ten'),
    # 887. 堂
    (u'どう', u'dō'),
    # 888. 連邦
    (u'れんぽう', u'renpō'),
    # 889. ビル
    (u'ビル', u'biru'),
    # 890. 体重
    (u'たいじゅう', u'taijū'),
    # 891. 新た
    (u'あらた', u'arata'),
    # 892. 語る
    (u'かたる', u'kataru'),
    # 893. 神奈川
    (u'かながわ', u'kanagawa'),
    # 894. 兵庫
    (u'ひょうご', u'hyōgo'),
    # 895. 木
    (u'もく', u'moku'),
    # 896. 挙げる
    (u'あげる', u'ageru'),
    # 897. 本部
    (u'ほんぶ', u'honbu'),
    # 898. 専用
    (u'せん|よう', u'senyō'),
    # 899. 運用
    (u'うん|よう', u'unyō'),
    # 900. 佐藤
    (u'', u''),
    # 901. 結成
    (u'けっせい', u'kessei'),
    # 902. 試験
    (u'しけん', u'shiken'),
    # 903. 組合
    (u'くみあい', u'kumiai'),
    # 904. 福島
    (u'ふくしま', u'fukushima'),
    # 905. 原
    (u'げん', u'gen'),
    # 906. 言葉
    (u'ことば', u'kotoba'),
    # 907. 当
    (u'とう', u'tō'),
    # 908. 亜
    (u'あ', u'a'),
    # 909. 生徒
    (u'せいと', u'seito'),
    # 910. 沿革
    (u'えんかく', u'enkaku'),
    # 911. ネット
    (u'ネット', u'netto'),
    # 912. 求める
    (u'もとめる', u'motomeru'),
    # 913. 移籍
    (u'いせき', u'iseki'),
    # 914. ゲスト
    (u'ゲスト', u'gesuto'),
    # 915. 連載
    (u'れんさい', u'rensai'),
    # 916. 資料
    (u'し|りょう', u'shiryō'),
    # 917. 事故
    (u'じこ', u'jiko'),
    # 918. 正式
    (u'せいしき', u'seishiki'),
    # 919. 電話
    (u'でんわ', u'denwa'),
    # 920. ノ
    (u'ノ', u'no'),
    # 921. 効果
    (u'こう|か', u'kōka'),
    # 922. 追加
    (u'ついか', u'tsuika'),
    # 923. 登録
    (u'とう|ろく', u'tōroku'),
    # 924. わ
    (u'わ', u'wa'),
    # 925. 業務
    (u'ぎょう|む', u'gyōmu'),
    # 926. 説
    (u'せつ', u'setsu'),
    # 927. コース
    (u'コース', u'kōsu'),
    # 928. 労働
    (u'ろう|どう', u'rōdō'),
    # 929. 私
    (u'あたし', u'atashi'),
    # 930. 医療
    (u'い|りょう', u'iryō'),
    # 931. 静岡
    (u'しずおか', u'shizuoka'),
    # 932. 制度
    (u'せいど', u'seido'),
    # 933. な
    (u'な', u'na'),
    # 934. ちる
    (u'ちる', u'chiru'),
    # 935. 学生
    (u'がく|せい', u'gakusei'),
    # 936. 変化
    (u'へんか', u'henka'),
    # 937. 良い
    (u'よい', u'yoi'),
    # 938. ベース
    (u'ベース', u'bēsu'),
    # 939. 残る
    (u'のこる', u'nokoru'),
    # 940. アナウンサー
    (u'アナウンサー', u'anaunsā'),
    # 941. 死去
    (u'しきょ', u'shikyo'),
    # 942. 市場
    (u'いち|ば', u'ichiba'),
    # 943. ステージ
    (u'ステージ', u'sutēji'),
    # 944. 弾
    (u'たま', u'tama'),
    # 945. 残す
    (u'のこす', u'nokosu'),
    # 946. 決勝
    (u'けっ|しょう', u'kesshō'),
    # 947. 盤
    (u'さら', u'sara'),
    # 948. 博士
    (u'はかせ', u'hakase'),
    # 949. まま
    (u'まま', u'mama'),
    # 950. 王国
    (u'おう|こく', u'ōkoku'),
    # 951. 向かう
    (u'むかう', u'mukau'),
    # 952. レース
    (u'レース', u'rēsu'),
    # 953. 大臣
    (u'だいじん', u'daijin'),
    # 954. 生物
    (u'せいぶつ', u'seibutsu'),
    # 955. 黒
    (u'くろ', u'kuro'),
    # 956. 兵
    (u'いくさ', u'ikusa'),
    # 957. とる
    (u'とる', u'toru'),
    # 958. 中村
    (u'なかむら', u'nakamura'),
    # 959. ほぼ
    (u'ほぼ', u'hobo'),
    # 960. 帯
    (u'たい', u'tai'),
    # 961. 楽曲
    (u'がっきょく', u'gakkyoku'),
    # 962. よく
    (u'よく', u'yoku'),
    # 963. 詳細
    (u'しょう|さい', u'shōsai'),
    # 964. 美術
    (u'びじゅつ', u'bijutsu'),
    # 965. 歌手
    (u'かしゅ', u'kashu'),
    # 966. 座
    (u'ざ', u'za'),
    # 967. 規模
    (u'きぼ', u'kibo'),
    # 968. です
    (u'です', u'desu'),
    # 969. 声優
    (u'せいゆう', u'seiyū'),
    # 970. 仙台
    (u'せんだい', u'sendai'),
    # 971. 長崎
    (u'ながさき', u'nagasaki'),
    # 972. 全体
    (u'ぜんたい', u'zentai'),
    # 973. 刑事
    (u'けいじ', u'keiji'),
    # 974. 競走
    (u'きょう|そう', u'kyōsō'),
    # 975. クラス
    (u'クラス', u'kurasu'),
    # 976. 砲
    (u'じゅう', u'jū'),
    # 977. く
    (u'く', u'ku'),
    # 978. 沖縄
    (u'おきなわ', u'okinawa'),
    # 979. 陸上
    (u'りく|じょう', u'rikujō'),
    # 980. ジャンル
    (u'ジャンル', u'janru'),
    # 981. あるいは
    (u'あるいは', u'aruiha'),
    # 982. アジア
    (u'アジア', u'ajia'),
    # 983. 葉
    (u'は', u'ha'),
    # 984. 店舗
    (u'てんぽ', u'tenpo'),
    # 985. 市民
    (u'しみん', u'shimin'),
    # 986. 社名
    (u'しゃめい', u'shamei'),
    # 987. 好き
    (u'すき', u'suki'),
    # 988. 九
    (u'チュー', u'chū'),
    # 989. 複数
    (u'ふくすう', u'fukusū'),
    # 990. 入り
    (u'いり', u'iri'),
    # 991. 死
    (u'し', u'shi'),
    # 992. 熊本
    (u'くまもと', u'kumamoto'),
    # 993. 戻る
    (u'もどる', u'modoru'),
    # 994. つける
    (u'つける', u'tsukeru'),
    # 995. 左
    (u'さ', u'sa'),
    # 996. 銀行
    (u'ぎん|こう', u'ginkō'),
    # 997. 以来
    (u'いらい', u'irai'),
    # 998. 白
    (u'しら', u'shira'),
    # 999. メイン
    (u'メイン', u'mein'),
    # 1000. もと
    (u'もと', u'moto')
]
