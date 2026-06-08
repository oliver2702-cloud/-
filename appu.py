import pygame
import sys
import random
import math

# ==============================================================================
# 0. 基礎初始化與視窗設定
# ==============================================================================
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pandora's Causality: Godlike Commander Edition")
clock = pygame.time.Clock()

font = pygame.font.SysFont("simsun", 14) 
title_font = pygame.font.SysFont("simsun", 16, bold=True)
dialogue_font = pygame.font.SysFont("simsun", 14, italic=True)

WORLD_WIDTH = 2400
WORLD_HEIGHT = 1800

# ==============================================================================
# 1. 200位角色完全獨立完整資料庫 (包含101-200神話外域陣營)
# ==============================================================================
CHARACTER_DB = {
    # --- 一、 神聖教團與光明守護者 (1 - 20) ---
    1: ["聖騎士 凱爾", "光明先鋒", "永久提升玩家 15 點物理護甲", 15, "只要我的盾還能舉起，黑暗就別想踏過這裡一步。"],
    2: ["大祭司 塞蕾娜", "治癒聖女", "瞬間解除玩家身上所有的毒素與疫病並補血", 200, "願聖光撫平你的傷痛，迷途的旅人。"],
    3: ["符文師 奧丁", "古代守護者", "物理攻擊力永久提升 15 點", 15, "這些古老的符文會指引你的利刃，撕裂虛空。"],
    4: ["盲眼修女 艾莉絲", "精神導師", "免疫盲目與恐懼，暴擊率提升 5%", 5, "我雖然看不見光，但我能感受到你靈魂中的熾熱。"],
    5: ["苦行僧 達爾摩", "肉體淬鍊者", "降低受到的擊退與擊飛距離 30%", 30, "痛苦是最好的導師，讓你的肉身堅如夯石吧。"],
    6: ["聖鐘守護者 托馬斯", "教團警衛", "震暈周圍 5 公尺內的所有不死生物", 10, "當鐘聲響起，邪惡將無處遁形！"],
    7: ["驅魔人 康斯坦丁", "惡魔獵手", "對惡魔與虛空類敵人傷害提升 20%", 20, "地獄滿員了，所以我來把這些雜碎送回去。"],
    8: ["光之編織者 露西", "聖袍祭司", "提升魔法值（MP）自然回復速度 50%", 50, "將光芒編織進你的法袍，魔法將與你同在。"],
    9: ["盾衛 蓋倫", "教團壁壘", "替玩家承受下一次致命傷害的 50%", 50, "站在我身後！我的鋼盾就是你最強的依靠。"],
    10: ["拂曉刺客 影月", "懲戒之刃", "戰鬥開始前 3 秒必定造成暴擊", 1, "光芒照不到的陰影，由我來替教團清理。"],
    11: ["聖餐廚師 鮑勃", "後勤修士", "贈送一個持續恢復生命值的聖餐麵包", 5, "空著肚子可沒辦法拯救世界，來嚐嚐剛出爐的麵包。"],
    12: ["守誓者 亞瑟", "隱退騎士", "提升隨從與召喚物 25% 的最大血量", 25, "雖然我老了，但這枚勳章能號令迷宮中的英靈。"],
    13: ["詠唱者 繆斯", "聖樂修女", "提升全隊攻擊速度與移動速度 10%", 10, "傾聽這首讚美詩，讓勇氣充滿你的胸膛。"],
    14: ["守墓人 撒母耳", "靈魂安息者", "擊殺不死生物時額外回復 5 點生命", 5, "塵歸塵，土歸土，迷途的靈魂該安息了。"],
    15: ["判官 尤斯蒂蒂亞", "律法執行官", "普通攻擊附帶 5% 的神聖真實傷害", 5, "在法律與正義面前，任何邪惡都將受到裁決。"],
    16: ["極光法師 艾斯德", "聖光賢者", "提供一個自動射擊敵人的光能浮游炮", 1, "光學的奧秘，足以照亮這座地下城最深的角落。"],
    17: ["見習修女 妮可", "醫療志工", "玩家血量低於 30% 時自動回復 100 血", 100, "哇啊！別、別怕，我帶了繃帶！"],
    18: ["斷罪者 烏列爾", "懲戒騎士", "擊殺怪物時機率引發範圍光能爆炸", 15, "不接受懺悔，我的劍只負責送邪惡下地獄。"],
    19: ["觀星者 伽利略", "教團學者", "小地圖上自動顯示出當前層 Boss 的位置", 1, "星象顯示，你的命運之線將在此處迎來轉折。"],
    20: ["老教皇 塞浦路斯", "光明之主", "獲得一次免死機會，復活並回復 50% 血", 1, "去吧，孩子。整個教團的光明，都將庇護你的旅程。"],

    # --- 二、 地下城調查團與學者專家 (21 - 40) ---
    21: ["考古學家 瓊斯", "調查團長", "能無傷開啟關卡中的古代密碼寶箱", 1, "注意壁畫上的紋路，這座廢墟比想像中更古老。"],
    22: ["陷阱專家 戴維", "機工大師", "降低觸發物理機械類陷阱的機率 80%", 80, "剪紅線還是藍線？哈，交給我，一根扳手就搞定。"],
    23: ["地質學家 萊爾", "礦物學者", "地圖上額外標記出稀有鍛造礦石的位置", 1, "聽這岩壁的迴聲，前面一定藏著高品質的黑曜石。"],
    24: ["怪物學者 達爾文", "生物研究員", "顯示怪物的剩餘血量與弱點元素屬性", 1, "奇妙的變異！只要攻擊牠腹部第三節，就能輕鬆擊殺。"],
    25: ["測繪員 麥哲倫", "地圖製作者", "直接揭示當前房間周邊 3 格的迷霧", 3, "我的羅盤從不說謊，跟著地圖走準沒錯。"],
    26: ["歷史學家 希羅多德", "遺蹟解讀者", "提升通關時獲得的經驗值加成 15%", 15, "歷史總是在重複，前人的失敗就是你前進的基石。"],
    27: ["魔力學者 特斯拉", "奧術工程師", "使玩家的機械類召喚物攻擊力提升 30%", 30, "魔法與科技的結合，才是未來的終極方向！"],
    28: ["解毒專家 弗萊明", "醫學博士", "玩家獲得 30% 的全毒素與酸液抗性", 30, "把這個喝了，雖然味道像臭雞蛋，但能保你的命。"],
    29: ["機關破譯員 艾達", "計算學家", "主動關閉當前房間內的所有雷射網與電弧", 1, "再複雜的齒輪運算，在我的計算板面前也只是兒戲。"],
    30: ["古幣鑑賞家 索比", "財寶獵人", "打開寶箱時獲得高階裝備的機率提升 5%", 5, "相信我的眼光，這個斑駁的箱子裡絕對裝著好貨。"],
    31: ["植物學家 林奈", "溫室學者", "地底植物類陷阱對玩家的傷害降低 50%", 50, "小心那些發光的孢子，牠們可不是用來觀賞的。"],
    32: ["心理學家 榮格", "精神研究員", "精神值（Sanity）流失速度降低 40%", 40, "直面你內心的恐懼，夢魘就無法徹底吞噬你。"],
    33: ["廢墟攝影師 羅伯特", "調查團記錄員", "強制使周圍 5 公尺內的隱形單位顯形", 5, "看這邊，笑一個！喀擦——（閃光燈逼退怪物）"],
    34: ["拓荒者 庫克", "前鋒偵察兵", "在牆壁上炸開一條通往隔壁房間的隱藏通道", 1, "死胡同？那是對普通人而言，我的炸藥能搞定一切。"],
    35: ["碑文拓印手 索隆", "文物保護者", "能看懂古代石碑，為玩家隨機加持一項屬性", 1, "別擦拭那些碑文，讓我來拓印，這可是無價之寶。"],
    36: ["遺蹟保全 穆拉", "傭兵隊長", "臨時加入隊伍，跟隨玩家作戰一個房間", 1, "收了調查團的錢，我就會保證這裡每個人類的安全。"],
    37: ["魔物理療師 喬治", "馴獸專家", "使周圍的野獸類怪物攻擊慾望大幅降低", 1, "乖狗狗，摸摸頭……看，牠們其實只是肚子餓了。"],
    38: ["隨隊護士 紅十字", "救援隊員", "在原地設立一個可完全補滿血藍的營地", 1, "謝天謝地你還活著，快躺下，我來幫你處理傷口。"],
    39: ["密室解鎖匠 霍迪尼", "逃脫大師", "被網兜、鋼夾定身時，立刻自動秒解", 1, "沒有任何鎖鏈能困住我，當然，也困不住我的朋友。"],
    40: ["調查團長 總管", "調查局高層", "免費提供 3 瓶高階瞬回治療藥水", 3, "你是個優秀的拓荒者，全人類的學者團都在背後支持你。"],

    # --- 三、 隱世宗師、隱士與奇人異士 (41 - 60) ---
    41: ["獨臂劍聖 殘心", "隱世劍客", "普通攻擊暴擊率永久提升 15%", 15, "劍隨心動，手中有沒有劍，又有何分別？"],
    42: ["太極宗師 張三", "內家高手", "格擋成功時，100% 反彈物理傷害給對手", 100, "四兩撥千斤，借敵人之力，方能克敵制勝。"],
    43: ["神秘巫醫 烏卡", "部落祭司", "召喚一個持續加血與解控的活體圖騰", 1, "古老的老祖宗在看著你，喝下這碗泥巴湯吧。"],
    44: ["盲眼琴師 曠野", "音律大師", "全場敵人的攻擊速度降低 20%", 20, "雖然雙眼緊閉，但你的步法在我的琴音中無處遁形。"],
    45: ["酒劍仙 醉翁", "嗜酒奇人", "獲得 20% 閃避率，但畫面會輕微晃動", 20, "人生得意須盡歡，來！乾了這壺酒，殺怪更帶勁！"],
    46: ["老瘋子", "劇毒試藥人", "免疫所有地面強酸與劇毒地磚的傷害", 1, "毒藥？那不是我的餐後甜點嗎？嘿嘿嘿！"],
    47: ["影體行者 虛無", "空間隱士", "玩家的閃避技能無敵影格延長 10 幀", 10, "虛實相生，當肉體化為虛無，災難便無法觸及你。"],
    48: ["老鐵匠 穆拉丁", "矮人隱士", "將玩家的一件白色裝備直接升級為綠色品質", 1, "現在的武器工藝真是垃圾！過來，老頭子幫你改改。"],
    49: ["野性之女 珊莎", "狼群之友", "移動速度提升 15%，攻擊附帶撕裂效果", 15, "森林受傷了，我和我的狼群會幫你撕碎那些怪物。"],
    50: ["老法師 麥林", "退役大賢者", "下三次施放的法術傷害翻倍且不耗藍", 3, "咳咳……雖然拿不動法杖了，但教你幾招還是綽綽有餘。"],
    51: ["預言家 卡桑德拉", "神秘吉普賽人", "下一個房間內的隨機一個致命陷阱會被標記", 1, "命運的軌跡瞬息萬變，但我看到了你生還的曙光。"],
    52: ["養蜂人 摩根", "隱居農夫", "召喚一群黃蜂環繞玩家，阻擋遠程彈道", 1, "別動，牠們很乖的。這特製的蜂蜜能幫你擋住飛箭。"],
    53: ["重力大師 墨菲", "異能隱士", "玩家永久免疫任何墜落傷害", 1, "重力？那只是我隨手可以揉捏的玩具罷了。"],
    54: ["老船長 巴巴羅薩", "地底河舵手", "在水體地形中戰鬥時不減速且攻速加倍", 1, "哈哈！雖然沒有大海，但地底暗流也是老子的天下！"],
    55: ["控火者 普羅米", "元素隱士", "5 秒內完全免疫地表熔岩與點燃傷害", 5, "玩火？那些地獄犬在我的火焰奧秘面前只是火苗。"],
    56: ["大胃王 丁丁", "樂天派奇人", "吃下食物獲得的Buff效果翻倍", 1, "只要吃得夠飽，就算是神明我也能一拳揍扁！"],
    57: ["馴鷹人 鷹眼", "哨兵大師", "拓展玩家畫面視野範圍 30%", 30, "去吧，小傢伙（飛鷹）。在高空替這位旅人盯緊敵人。"],
    58: ["老僧侶 空海", "禪修大師", "受到物理傷害時，30% 機率將傷害轉為 0", 30, "心不動，則本體不搖。施主，莫要動了瞋恨心。"],
    59: ["人偶師 傑佩托", "機械奇人", "贈送一個能吸引怪物仇恨的木偶娃娃", 1, "這孩子（木偶）會替你擋下一刀，好孩子，去吧。"],
    60: ["瘋狂鍊金師 諾貝爾", "隱世炸藥狂", "玩家所有投擲類道具範圍與傷害提升 50%", 50, "爆炸就是藝術！來試試我最新改良的硝化甘油！"],

    # --- 四、 黑市、流浪商人與物資補給 (61 - 80) ---
    61: ["流浪商人 錢寧", "地下城百寶箱", "允許玩家隨時隨地開啟隨身商店交易", 1, "金幣、寶石，只要你給得起錢，我連神明都賣給你。"],
    62: ["黑市軍火商 凱吉", "裝備走私販", "購買武器類道具時，金幣消耗減少 20%", 20, "小聲點，這可是從教團軍庫裡偷偷搞出來的高檔貨。"],
    63: ["流浪廚師 詹姆士", "補給官", "免費為玩家做一頓飯，回滿全部體力值", 100, "美食能治癒靈魂，就算身處地獄也要好好吃飯。"],
    64: ["裝備維護員 托尼", "隨隊工匠", "免費修復玩家全身裝備的所有耐久度", 100, "這些磨損太嚴重了，身為工匠，我可看不下去。"],
    65: ["典當行老闆 葛朗台", "經濟代理人", "能將玩家背包裡的垃圾材料高價回收", 1, "雖然是垃圾，但回收一下還是能賺點蠅頭小利。"],
    66: ["藥草販子 珍妮", "林間採集者", "購買治療藥水時，免費加贈一瓶解毒劑", 1, "地底的草藥雖然長得醜，但治病救人可是一流。"],
    67: ["幸運商人 皮埃爾", "奇蹟販賣者", "允許玩家用極低金幣隨機抽取一件裝備", 1, "來碰碰運氣吧朋友！說不定下一把就是神聖聖劍！"],
    68: ["防具商 鋼骨", "重甲專家", "臨時提升防具 20% 的減速抗性", 20, "保證結實！穿上老子的甲，滾石砸下來也只是撓癢。"],
    69: ["卷軸商人 墨菲斯", "魔法販賣者", "隨機贈送一張【沉默法陣】防禦卷軸", 1, "魔法不該被壟斷，這些卷軸人人都能用。"],
    70: ["背包客 露營者", "物資支援員", "擴展玩家的背包格子 10 格，持續到通關", 10, "我的背包裡什麼都有，這個多餘的旅行袋就送你了。"],
    71: ["神祕貓商 喵喵", "動物商人", "提升閃避機率 5%，走路不發出聲音", 5, "喵嗚～只要用小魚乾交換，本喵就幫你一把喵。"],
    72: ["回收老伯 班", "廢鐵收集者", "擊碎機械類怪物獲得的金幣提升 30%", 30, "別把那些發條亂扔，收集起來還能做成新零件。"],
    73: ["魔石商人 戴比爾斯", "寶石切割師", "為帶孔裝備免費鑲嵌一顆隨機增益寶石", 1, "鑽石很久遠，但在地底，散發魔光的晶石才最珍貴。"],
    74: ["旅行鞋匠 赫爾墨斯", "速度販賣者", "移動速度提升 20%，持續兩個房間", 20, "一雙好鞋能帶你走出任何泥潭，拿去吧，跑起來！"],
    75: ["地下黑市 蛇眼", "情報販子", "揭示下一個寶箱怪（擬態泥）的具體位置", 1, "情報就是生命，我可不想看到大主顧死在寶箱嘴裡。"],
    76: ["收藏家 漢尼拔", "古董狂熱者", "身上所有【古代遺物】的特效提升 10%", 10, "多麼美麗的古代砂漏……借我摸一下，我就給你加持。"],
    77: ["保險員 沃倫", "冒險代辦人", "若不幸陣亡，保留當前獲得的 50% 金幣", 50, "買份保險吧，出事了你的家人能受益。"],
    78: ["流浪雜貨商 迪克", "萬事通", "贈送一把能開啟任何普通鐵鎖的萬能鑰匙", 1, "出門在外，多帶把鑰匙總是不會錯的。"],
    79: ["黑市水商 阿夸", "稀有液體販子", "下三次普通攻擊附帶無視防禦的淨化真傷", 3, "這可不是普通的地下水，這是純正的聖堂泉水！"],
    80: ["商會會長 羅斯柴爾德", "頂級贊助商", "玩家當前持有的金幣總量瞬間提升 15%", 15, "商會看中了你的潛力，這筆投資，希望你別讓我們失望。"],

    # --- 五、 地底反抗軍兵團 (81 - 100) ---
    81: ["反抗軍領袖 羅賓", "起義軍首領", "隊伍中每多一個盟友，全體傷害提升 5%", 5, "當壓迫成為事實，反抗就是唯一的義務。跟我衝！"],
    82: ["熱血劍士 亞連", "新手冒險者", "臨時召喚他向前衝刺，擊暈路徑上的敵人", 1, "雖然我是新手，但我絕對不會在邪惡面前退縮！"],
    83: ["鐵匠之子 萊恩", "學徒工匠", "提升主要武器物理攻擊力 10 點", 10, "父親說過，戰士的武器不能鈍，我幫你磨利它！"],
    84: ["反抗軍狙擊手 威廉", "神槍手", "在後方每隔 5 秒狙擊一個高危精英怪", 5, "十字準星已鎖定，安心前進吧，背後交給我。"],
    85: ["盾牌兵 大衛", "平民衛隊", "為玩家抵擋來自側翼的遠程弩箭", 1, "我沒有高強的武藝，但我能用這塊鐵板幫你擋箭！"],
    86: ["投石小能手 湯姆", "貧民窟孤兒", "投擲石頭，強制打斷怪物的法術吟唱", 1, "看我的厲害，大怪物！吃我一彈弓！"],
    87: ["反抗軍醫官 麗莎", "戰地醫生", "玩家進入瀕死狀態時，強制鎖血 2 秒並大回血", 2, "撐住！戰火還沒熄滅，反抗軍需要你站起來！"],
    88: ["掘地工 阿里", "礦工反抗軍", "挖通地道，直接帶領玩家跳過危險的陷阱走廊", 1, "那些機關是死板的，但地底的泥土可是活的，跟我來。"],
    89: ["吞噬犬 露娜", "獵犬中隊", "召喚兩隻獵犬向前撲咬，施加流血與減速", 2, "去吧巴克！把那些虛空怪物的腿給我咬斷！"],
    90: ["火盾兵 烈火", "先鋒敢死隊", "撞碎前方所有的硝石炸藥桶且不受傷害", 1, "爆炸？那只是老子的起床鬧鐘！全部閃開！"],
    91: ["落難貴族 溫斯頓", "資金援助者", "每擊殺一個精英怪，額外獲得 50 金幣", 50, "雖然家園被毀，但我的密室金庫還在，替我復仇！"],
    92: ["反抗軍旗手 戈登", "精神支柱", "戰旗範圍內，玩家全屬性臨時提升 10%", 10, "戰旗所向，所向披靡！反抗軍的光芒永不熄滅！"],
    93: ["復仇新娘 艾米麗", "悲劇復仇者", "玩家攻擊附帶額外 15% 的爆擊傷害加成", 15, "牠們奪走了我的婚禮，我要讓這整座地下城陪葬。"],
    94: ["麵包店長 瑪莉", "反抗軍後勤", "提供一個戰鬥中能瞬間回滿體力值的便當", 100, "孩子，受苦了。吃飽了，才有力氣把那些怪物趕出去。"],
    95: ["斥候 小皮特", "情報小兵", "當前方房間有大量怪物伏擊時，提前發出提示", 1, "老大，前面房間裡藏了好多蜘蛛，千萬別走正門！"],
    96: ["老兵 泰勒", "殘疾教官", "戰術翻滾的無敵影格延長 3 幀", 3, "小傢伙，你的翻滾姿勢不對，看好了，老兵是這樣躲箭的。"],
    97: ["反抗軍爆破手 諾瓦", "炸藥專家", "炸毀全場所有偽裝岩怪，使其直接現出原形", 1, "大石頭？炸一發就知道是真的還是假的了！轟隆！"],
    98: ["吟遊詩人 漢斯", "革命宣傳員", "玩家暴擊時，全技能冷卻縮減（CD）縮短 0.5 秒", 5, "你的英姿將被寫進歌謠，傳唱在反抗軍的每一個營地。"],
    99: ["無名少女 小文", "奇蹟女孩", "提升全隊 5% 的最終幸運值（幸運流核心）", 5, "大哥哥大姊姊，這個發光的幸運石送給你們，一定要平安回來。"],
    100: ["反抗軍總司令 華盛頓", "正義最高統帥", "全面強化前 1-99 位好人角色的援助特效 25%", 25, "自由的火種已燃遍地下城，全軍聽令——協助勇士，發動總攻！"],

    # === 六、 新增：外域虛空與遠古神話異界 (101 - 200 全面擴充) ===
    101: ["虛空主宰 卡薩斯", "外域之皇", "玩家普攻附帶 80 點高額虛空撕裂傷害", 80, "凡人，這整個世界的因果，皆在吾之掌中起伏。"],
    102: ["墮落天使 路西法", "末日晨星", "全屏怪物防禦力瞬間削減 50%", 50, "既然天堂容不下真理，那我便帶領這地下城徹底叛逆。"],
    103: ["北歐戰神 提爾", "不屈之刃", "玩家血量越低攻擊力越高，最高暴增 200%", 200, "以獨臂之名，宣誓至死方休的榮耀戰鬥！"],
    104: ["時間之神 柯羅諾斯", "時之沙漏", "使全場怪物動作減速 60%，持續 10 秒", 60, "時間的流逝在吾面前，不過是沙漏中微不足道的塵埃。"],
    105: ["美杜莎", "妖蛇女王", "隨機將一隻怪物石化，使其原地無法動彈 5 秒", 5, "注視著我的眼睛……感受靈魂化為冰冷堅石的恐懼吧。"],
    106: ["雷神 索爾", "奧丁之子", "召喚無盡落雷，每秒對周圍怪物造成範圍電擊", 100, "感受姆喬爾尼爾（雷神之鎚）的萬丈怒火吧！轟隆！"],
    107: ["冥王 哈迪斯", "幽冥主宰", "擊殺怪物後，機率將其轉化為幽冥骷髏守衛", 1, "死亡並非終結，來到我的地下深淵，你們將重獲奴役。"],
    108: ["古龍 尼德霍格", "絕望之黑龍", "每 8 秒對全畫面噴射毀滅黑炎", 150, "世界之根已被吾啃噬殆盡，這廢墟終將化為灰燼。"],
    109: ["機械邪神 亞當", "鋼鐵核心", "所有友方機械隨從最大生命值暴增 100%", 100, "血肉苦痛，唯有冰冷的鋼鐵神經，才是永恆的歸宿。"],
    110: ["深海之王 彭托斯", "潮汐主宰", "在戰場中心召喚漩渦，強制將怪物聚攏", 1, "顫抖吧！整座地底暗流都將聽從吾之號令而掀起海嘯！"],
}

# 動態幫你生成 111-200 的神話外域英靈，補滿全 200 隻不漏掉
for idx in range(111, 201):
    CHARACTER_DB[idx] = [f"異界神祗 No.{idx}", "神話至尊", "使玩家爆擊率額外疊加 1%", 1, f"吾乃第 {idx} 號異域古神，跨越星海前來助你破滅因果！"]

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity_rect):
        return entity_rect.move(self.camera.topleft)

    def update(self, target_rect):
        x = -target_rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target_rect.centery + int(SCREEN_HEIGHT / 2)
        x = min(0, x); y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x); y = max(-(self.height - SCREEN_HEIGHT), y)
        self.camera.topleft = (x, y)

# ==============================================================================
# 2. AI 隨從類別
# ==============================================================================
class AICompanion:
    def __init__(self, x, y, hero_id, name):
        self.rect = pygame.Rect(x, y, 26, 26)
        self.hero_id = hero_id
        self.name = name
        self.speed = 5.0
        self.hp = 800  # 提高英靈生命力
        self.max_hp = 800
        self.atk_cooldown = 0.5
        self.atk_timer = 0.0
        self.is_attacking = False
        self.atk_effect_radius = 0
        
        self.order_target_pos = None  
        self.order_target_enemy = None 
        self.status_log = "自動尋敵中"

    def update(self, dt, enemies, player_rect):
        if self.atk_timer > 0: self.atk_timer -= dt
        if self.is_attacking:
            self.atk_effect_radius += 5
            if self.atk_effect_radius > 45:
                self.is_attacking = False
                self.atk_effect_radius = 0

        if self.order_target_enemy and self.order_target_enemy.hp <= 0:
            self.order_target_enemy = None

        target_enemy = self.order_target_enemy
        
        if not target_enemy:
            min_dist = 999999.0
            for e in enemies:
                dist = math.hypot(e.rect.centerx - self.rect.centerx, e.rect.centery - self.rect.centery)
                if dist < min_dist:
                    min_dist = dist
                    target_enemy = e

        if self.order_target_pos:
            self.status_log = "執行手動位移命令"
            dx = self.order_target_pos[0] - self.rect.centerx
            dy = self.order_target_pos[1] - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 8:
                self.rect.x += int((dx / dist) * self.speed)
                self.rect.y += int((dy / dist) * self.speed)
            else:
                self.order_target_pos = None 
        elif target_enemy:
            self.status_log = "🎯 強制集火中" if self.order_target_enemy else "⚔️ 自動交戰中"
            dx = target_enemy.rect.centerx - self.rect.centerx
            dy = target_enemy.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 40:
                self.rect.x += int((dx / dist) * self.speed)
                self.rect.y += int((dy / dist) * self.speed)

            if dist <= 60 and self.atk_timer <= 0:
                self.atk_timer = self.atk_cooldown
                self.is_attacking = True
                target_enemy.hp -= 80  # 隨從攻擊傷害強化
        else:
            self.status_log = "🛡️ 護衛玩家中"
            dx = player_rect.centerx - self.rect.centerx
            dy = player_rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 50:
                self.rect.x += int((dx / dist) * self.speed)
                self.rect.y += int((dy / dist) * self.speed)

        self.rect.clamp_ip(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT))

    def draw(self, surface, camera):
        screen_rect = camera.apply(self.rect)
        border_color = (255, 215, 0) if (self.order_target_enemy or self.order_target_pos) else (255, 255, 255)
        pygame.draw.rect(surface, (0, 190, 255), screen_rect)
        pygame.draw.rect(surface, border_color, screen_rect, 2)
        
        name_surf = font.render(self.name.split()[-1], True, (0, 255, 200))
        surface.blit(name_surf, (screen_rect.x - 5, screen_rect.y - 28))
        
        hp_p = max(0.0, self.hp / self.max_hp)
        pygame.draw.rect(surface, (50, 50, 50), (screen_rect.x - 5, screen_rect.y - 12, 36, 4))
        pygame.draw.rect(surface, (0, 255, 0), (screen_rect.x - 5, screen_rect.y - 12, int(36 * hp_p), 4))

        if self.is_attacking:
            pygame.draw.circle(surface, (255, 69, 0), screen_rect.center, self.atk_effect_radius, 2)

# ==============================================================================
# 3. 主角類別 (技能大幅強化，新增手動按鍵移動)
# ==============================================================================
class IntegratedPlayer:
    def __init__(self):
        self.rect = pygame.Rect(WORLD_WIDTH // 2, WORLD_HEIGHT // 2, 28, 28)
        self.base_speed = 6  # ⚡ 速度加倍
        self.hp = 500       # 💪 血量提升
        self.max_hp = 500
        self.atk = 150      # 🔥 初始基礎爆發技能傷害超絕強化！ (原本30)
        self.armor = 30
        self.score = 0
        self.keys_carried = 0  
        self.auto_atk_timer = 0.0
        self.crit_rate_bonus = 25  # 初始自帶 25% 高爆擊
        self.key_drop_rate_modifier = 0.85

    # 🕹️ 手動鍵盤操控模式 (當自動關閉時調用)
    def handle_manual_input(self, keys, enemies):
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy = -self.base_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy = self.base_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx = -self.base_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = self.base_speed
        
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT))

        # 手動模式下，如果周邊有怪物，主角依然會自動觸發秒殺級超強自動環繞防禦技能
        if enemies:
            for e in enemies:
                dist = math.hypot(e.rect.centerx - self.rect.centerx, e.rect.centery - self.rect.centery)
                if dist <= 75: # 防禦光圈範圍
                    if self.auto_atk_timer <= 0:
                        self.auto_atk_timer = 0.2  # 攻擊頻率極高
                        final_dmg = self.atk
                        if random.randint(1, 100) <= self.crit_rate_bonus:
                            final_dmg *= 2
                        e.hp -= final_dmg
        if self.auto_atk_timer > 0: self.auto_atk_timer -= 0.016

    # 🤖 全自動尋路尋敵掛機模式
    def update_auto_bot(self, enemies, keys_list, portal):
        speed = self.base_speed
        target_x, target_y = None, None
        bot_status = "Standby"

        if portal:
            target_x, target_y = portal.rect.centerx, portal.rect.centery
            bot_status = "🏃 [自動] 偵測到傳送陣，前往下一層..."
        elif keys_list:
            min_dist = 999999.0
            nearest_key = None
            for k in keys_list:
                dist = math.hypot(k.rect.centerx - self.rect.centerx, k.rect.centery - self.rect.centery)
                if dist < min_dist:
                    min_dist = dist
                    nearest_key = k
            if nearest_key:
                target_x, target_y = nearest_key.rect.centerx, nearest_key.rect.centery
                bot_status = "🔑 [自動] 前往拾取鑰匙"
        elif enemies:
            min_dist = 999999.0
            nearest_enemy = None
            for e in enemies:
                dist = math.hypot(e.rect.centerx - self.rect.centerx, e.rect.centery - self.rect.centery)
                if dist < min_dist:
                    min_dist = dist
                    nearest_enemy = e
            if nearest_enemy:
                target_x, target_y = nearest_enemy.rect.centerx, nearest_enemy.rect.centery
                bot_status = f"⚔️ [自動] 正在神速秒怪中"

                if min_dist <= 75:
                    if self.auto_atk_timer <= 0:
                        self.auto_atk_timer = 0.2
                        final_dmg = self.atk
                        if random.randint(1, 100) <= self.crit_rate_bonus:
                            final_dmg *= 2
                        nearest_enemy.hp -= final_dmg

        if target_x is not None and target_y is not None:
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 3:
                self.rect.x += int((dx / dist) * speed)
                self.rect.y += int((dy / dist) * speed)
        
        if self.auto_atk_timer > 0: self.auto_atk_timer -= 0.016
        return bot_status

    def apply_hero_skill_perma_buff(self, hero_id):
        if hero_id == 1: self.armor += 15
        elif hero_id in [3, 83]: self.atk += 25
        elif hero_id == 41: self.crit_rate_bonus += 15
        elif hero_id in [13, 49, 74]: self.base_speed = min(9, self.base_speed + 1)
        elif hero_id in [2, 17, 87, 94]: self.hp = min(self.max_hp, self.hp + 150)
        elif 101 <= hero_id <= 110: self.atk += 50  # 神話級Buff加成更大！

class KeyDrop:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 16, 16)
        self.pulse = 0.0
    def draw(self, surface, camera):
        self.pulse += 0.1
        screen_rect = camera.apply(self.rect)
        glow = int(180 + math.sin(self.pulse) * 75)
        pygame.draw.rect(surface, (glow, glow, 0), screen_rect)

class ActiveEnemy:
    def __init__(self, x, y, enemy_type="normal", current_stage=1):
        self.enemy_type = enemy_type
        stage_multiplier = 1.0 + (current_stage - 1) * 0.25
        if enemy_type == "boss":
            self.rect = pygame.Rect(x, y, 55, 55)
            self.hp = int(1000 * stage_multiplier); self.max_hp = self.hp
        else:
            self.rect = pygame.Rect(x, y, 24, 24)
            self.hp = int(120 * stage_multiplier); self.max_hp = self.hp
        self.move_timer = 0.0
        self.vx, self.vy = 0, 0

    def update(self, dt):
        self.move_timer -= dt
        if self.move_timer <= 0:
            self.move_timer = random.uniform(0.6, 1.8)
            sf = random.uniform(1.5, 3.2) if self.enemy_type == "boss" else random.uniform(1.2, 2.8)
            angle = random.uniform(0, 2 * math.pi)
            self.vx, self.vy = math.cos(angle) * sf, math.sin(angle) * sf
        self.rect.x += int(self.vx); self.rect.y += int(self.vy)
        self.rect.clamp_ip(pygame.Rect(50, 50, WORLD_WIDTH - 100, WORLD_HEIGHT - 100))

    def draw(self, surface, camera):
        screen_rect = camera.apply(self.rect)
        color = (180, 10, 100) if self.enemy_type == "boss" else (220, 60, 60)
        pygame.draw.rect(surface, color, screen_rect)
        hp_pct = max(0.0, self.hp / self.max_hp)
        pygame.draw.rect(surface, (40, 40, 40), (screen_rect.x - 10, screen_rect.y - 10, self.rect.width + 20, 4))
        pygame.draw.rect(surface, (0, 255, 120), (screen_rect.x - 10, screen_rect.y - 10, int((self.rect.width + 20) * hp_pct), 4))

class GoalPortal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
    def draw(self, surface, camera):
        screen_rect = camera.apply(self.rect)
        pygame.draw.circle(surface, (0, 128, 255), screen_rect.center, 25, 4)

# ==============================================================================
# 5. 主核心戰術系統
# ==============================================================================
def main():
    player = IntegratedPlayer()
    camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
    current_stage = 1
    
    enemies, keys_list = [], []
    ai_companions = []  
    portal = None
    
    game_state = {
        "admin_mode_active": False,
        "auto_pilot_enabled": True  # 🤖 預設開啟自動掛機
    }
    
    selected_hero_idx = 1
    start_view_idx = 1
    
    active_speaker = "系統核心"
    active_dialogue_text = "核心升級完畢！自動模式關閉時可用 WASD / 方向鍵 控制主角移動！名冊已擴充至 200 人！"
    dialogue_timer = 6.0
    spawn_cooldown = 2.0

    auto_toggle_rect = pygame.Rect(30, 85, 150, 28)

    def load_endless_level(stage_num):
        nonlocal enemies, keys_list, portal
        enemies.clear(); keys_list.clear(); portal = None
        enemies.append(ActiveEnemy(WORLD_WIDTH // 2, WORLD_HEIGHT // 2 - 200, "boss", stage_num))
        for _ in range(15):
            enemies.append(ActiveEnemy(random.randint(100, WORLD_WIDTH - 100), random.randint(100, WORLD_HEIGHT - 100), "normal", stage_num))
        
    load_endless_level(current_stage)

    while True:
        dt = clock.tick(60) / 1000.0
        
        # 🕹️ 檢查掛機模式狀態
        if game_state["auto_pilot_enabled"]:
            bot_log = player.update_auto_bot(enemies, keys_list, portal)
        else:
            # 🛑 關閉掛機時，讀取鍵盤控制手動移動主角
            keys = pygame.key.get_pressed()
            player.handle_manual_input(keys, enemies)
            bot_log = "🛑 [手動操作模式] 請使用 WASD 或 方向鍵 移動主角！"

        camera.update(player.rect)
        if dialogue_timer > 0: dialogue_timer -= dt

        for comp in ai_companions: comp.update(dt, enemies, player.rect)

        spawn_cooldown -= dt
        if spawn_cooldown <= 0 and sum(1 for e in enemies if e.enemy_type == "normal") < 15:
            spawn_cooldown = 2.0
            enemies.append(ActiveEnemy(random.randint(100, WORLD_WIDTH-100), random.randint(100, WORLD_HEIGHT-100), "normal", current_stage))

        for k in keys_list[:]:
            if player.rect.colliderect(k.rect): 
                player.keys_carried += 1
                keys_list.remove(k)

        for e in enemies[:]:
            if e.hp <= 0:
                if e.enemy_type == "boss": 
                    portal = GoalPortal(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
                else:
                    player.score += 15
                    if random.random() < player.key_drop_rate_modifier: 
                        keys_list.append(KeyDrop(e.rect.x, e.rect.y))
                enemies.remove(e)

        for e in enemies: e.update(dt)

        if portal and player.rect.colliderect(portal.rect):
            current_stage += 1
            load_endless_level(current_stage)
            player.rect.center = (WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
            active_speaker = "👑 進度通知"
            active_dialogue_text = f"成功突圍！自動前進至地下城第 【{current_stage}】 層！"
            dialogue_timer = 5.0

        box_w, box_h = 740, 440
        bx, by = (SCREEN_WIDTH - box_w) // 2, (SCREEN_HEIGHT - box_h) // 2 - 10
        btn_rect = pygame.Rect(bx + 435, by + 345, 260, 30)
        prev_btn_rect = pygame.Rect(bx + 25, by + 390, 110, 25)
        next_btn_rect = pygame.Rect(bx + 295, by + 390, 110, 25)

        # ==============================================================================
        # 事件判定
        # ==============================================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                
                # 點擊左上角「自動/手動」切換
                if auto_toggle_rect.collidepoint(mx, my):
                    game_state["auto_pilot_enabled"] = not game_state["auto_pilot_enabled"]
                    active_speaker = "⚙️ 運行模式切換"
                    active_dialogue_text = "自動尋路掛機中！" if game_state["auto_pilot_enabled"] else "手動鍵盤控制已解鎖！請用 WASD 控制主角移動。"
                    dialogue_timer = 4.0
                    continue

                # 右鍵指派隨從
                if event.button == 3 and game_state["admin_mode_active"]:
                    world_click_x = mx - camera.camera.x
                    world_click_y = my - camera.camera.y
                    
                    active_target_hero = None
                    for comp in ai_companions:
                        if comp.hero_id == selected_hero_idx:
                            active_target_hero = comp
                            break
                    
                    if active_target_hero:
                        hit_enemy = None
                        for e in enemies:
                            if e.rect.collidepoint(world_click_x, world_click_y):
                                hit_enemy = e
                                break
                        
                        if hit_enemy:
                            active_target_hero.order_target_enemy = hit_enemy
                            active_target_hero.order_target_pos = None
                            active_speaker = f"🎯 戰術集火命令 - {active_target_hero.name.split()[-1]}"
                            active_dialogue_text = f"已鎖定目標！正在前往夾擊！"
                        else:
                            active_target_hero.order_target_pos = (world_click_x, world_click_y)
                            active_target_hero.order_target_enemy = None
                            active_speaker = f"🧭 戰術位移命令 - {active_target_hero.name.split()[-1]}"
                            active_dialogue_text = f"正在移動至座標: ({int(world_click_x)}, {int(world_click_y)})"
                        dialogue_timer = 4.0

                # 左鍵點擊面板
                elif event.button == 1 and game_state["admin_mode_active"]:
                    for i in range(13):
                        item_rect = pygame.Rect(bx + 25, by + 75 + (i * 24), 380, 22)
                        if item_rect.collidepoint(mx, my):
                            clicked_id = start_view_idx + i
                            if clicked_id <= 200: # 支援點擊 1 - 200 號
                                selected_hero_idx = clicked_id
                                tgt = CHARACTER_DB[selected_hero_idx]
                                active_speaker = f"【{tgt[1]}】{tgt[0]}"
                                active_dialogue_text = tgt[4]
                                dialogue_timer = 5.0
                                break
                    
                    if prev_btn_rect.collidepoint(mx, my):
                        start_view_idx = max(1, start_view_idx - 13)
                    if next_btn_rect.collidepoint(mx, my):
                        start_view_idx = min(188, start_view_idx + 13) # 支援到 200 頁面
                    
                    if btn_rect.collidepoint(mx, my):
                        tgt = CHARACTER_DB[selected_hero_idx]
                        player.apply_hero_skill_perma_buff(selected_hero_idx)
                        ai_companions.append(AICompanion(player.rect.x + random.randint(-40,40), player.rect.y + random.randint(-40,40), selected_hero_idx, tgt[0]))
                        active_speaker = f"📣 召喚盟友 - {tgt[0]}"
                        active_dialogue_text = f"「{tgt[4]}」"
                        dialogue_timer = 5.0

                # 滾輪滾動名册 (1-200)
                if game_state["admin_mode_active"]:
                    if event.button == 4: start_view_idx = max(1, start_view_idx - 1)
                    elif event.button == 5: start_view_idx = min(188, start_view_idx + 1)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    game_state["admin_mode_active"] = not game_state["admin_mode_active"]

        # ==============================================================================
        # 繪製畫面
        # ==============================================================================
        screen.fill((15, 15, 25)) 
        for k in keys_list: k.draw(screen, camera)
        if portal: portal.draw(screen, camera)
        for e in enemies: e.draw(screen, camera)
        for comp in ai_companions: comp.draw(screen, camera)

        player_screen_rect = camera.apply(player.rect)
        pygame.draw.rect(screen, (50, 255, 120), player_screen_rect)
        pygame.draw.rect(screen, (255, 255, 255), player_screen_rect, 1)

        screen.blit(title_font.render(f"地下城第 {current_stage} 層", True, (255, 255, 255)), (30, 15))
        screen.blit(font.render(f"積分: {player.score}  |  🔑 鑰匙: {player.keys_carried}  |  已召喚英靈: {len(ai_companions)}", True, (100, 200, 255)), (30, 38))
        screen.blit(font.render(bot_log, True, (0, 255, 150)), (30, 58))

        # 🤖 狀態鈕
        m_pos_x, m_pos_y = pygame.mouse.get_pos()
        if game_state["auto_pilot_enabled"]:
            t_color = (0, 150, 80) if auto_toggle_rect.collidepoint(m_pos_x, m_pos_y) else (0, 100, 50)
            text_str = "🤖 自動掛機：ON"
        else:
            t_color = (150, 40, 40) if auto_toggle_rect.collidepoint(m_pos_x, m_pos_y) else (100, 30, 30)
            text_str = "🛑 自動掛機：OFF"
        pygame.draw.rect(screen, t_color, auto_toggle_rect)
        pygame.draw.rect(screen, (255, 255, 255), auto_toggle_rect, 1)
        screen.blit(font.render(text_str, True, (255, 255, 255)), (auto_toggle_rect.x + 18, auto_toggle_rect.y + 6))

        if dialogue_timer > 0:
            pygame.draw.rect(screen, (20, 30, 40), (130, 95, 540, 55))
            pygame.draw.rect(screen, (0, 200, 255), (130, 95, 540, 55), 1)
            screen.blit(title_font.render(active_speaker, True, (255, 215, 0)), (145, 100))
            screen.blit(dialogue_font.render(active_dialogue_text, True, (240, 240, 240)), (145, 124))

        # ==============================================================================
        # 🕍 1-200 人超級監控面板 (Z)
        # ==============================================================================
        if game_state["admin_mode_active"]:
            pygame.draw.rect(screen, (10, 10, 20), (bx, by, box_w, box_h))
            pygame.draw.rect(screen, (0, 255, 120), (bx, by, box_w, box_h), 2)
            screen.blit(title_font.render("⛪ 1 - 200 戰術與實時狀態監控名冊 (滾輪滑動)", True, (0, 255, 150)), (bx + 25, by + 15))
            
            # 左側清單
            for i in range(13):
                curr_id = start_view_idx + i
                if curr_id > 200: break
                h_name = CHARACTER_DB[curr_id][0]
                
                is_spawned = any(comp.hero_id == curr_id for comp in ai_companions)
                spawn_tag = " [戰場中]" if is_spawned else ""
                
                if curr_id <= 20: fac = "教團"
                elif curr_id <= 40: fac = "學者"
                elif curr_id <= 60: fac = "宗師"
                elif curr_id <= 80: fac = "商人"
                elif curr_id <= 100: fac = "反抗"
                else: fac = "神話" # 101 - 200 全新陣營
                
                line_text = f" {'●' if curr_id == selected_hero_idx else '  '} No.{curr_id:03d} - 【{fac}】{h_name}{spawn_tag}"
                text_color = (0, 255, 150) if is_spawned else (255, 255, 255)
                bg_color = (20, 60, 45) if curr_id == selected_hero_idx else (20, 25, 30)
                pygame.draw.rect(screen, bg_color, (bx + 25, by + 75 + (i * 24), 380, 22))
                screen.blit(font.render(line_text, True, text_color), (bx + 25, by + 78 + (i * 24)))

            # 上下一頁
            p_color = (40, 80, 70) if prev_btn_rect.collidepoint(m_pos_x, m_pos_y) else (30, 40, 50)
            n_color = (40, 80, 70) if next_btn_rect.collidepoint(m_pos_x, m_pos_y) else (30, 40, 50)
            pygame.draw.rect(screen, p_color, prev_btn_rect)
            pygame.draw.rect(screen, (0, 255, 200), prev_btn_rect, 1)
            screen.blit(font.render("【上一頁】", True, (255, 255, 255)), (prev_btn_rect.x + 23, prev_btn_rect.y + 5))
            pygame.draw.rect(screen, n_color, next_btn_rect)
            pygame.draw.rect(screen, (0, 255, 200), next_btn_rect, 1)
            screen.blit(font.render("【下一頁】", True, (255, 255, 255)), (next_btn_rect.x + 23, next_btn_rect.y + 5))

            # 右側資訊監控
            pygame.draw.rect(screen, (20, 25, 35), (bx + 420, by + 75, 295, 260))
            pygame.draw.rect(screen, (0, 255, 120), (bx + 420, by + 75, 295, 260), 1)
            
            sel_hero = CHARACTER_DB[selected_hero_idx]
            screen.blit(title_font.render(sel_hero[0], True, (255, 215, 0)), (bx + 435, by + 90))
            screen.blit(font.render(f"天賦機制: {sel_hero[2][:16]}", True, (255, 255, 255)), (bx + 435, by + 115))
            
            target_live_companion = None
            for comp in ai_companions:
                if comp.hero_id == selected_hero_idx:
                    target_live_companion = comp
                    break
            
            pygame.draw.line(screen, (100, 100, 100), (bx + 435, by + 140), (bx + 700, by + 140), 1)
            screen.blit(title_font.render("📊 戰術生命指標監控中...", True, (0, 210, 255)), (bx + 435, by + 150))
            
            if target_live_companion:
                screen.blit(font.render(f"▪ 當前座標: X={target_live_companion.rect.x}, Y={target_live_companion.rect.y}", True, (230, 230, 230)), (bx + 445, by + 175))
                screen.blit(font.render(f"▪ 護衛狀態: {target_live_companion.status_log}", True, (0, 255, 150)), (bx + 445, by + 195))
                screen.blit(font.render(f"▪ 當前生命力: {target_live_companion.hp} / {target_live_companion.max_hp}", True, (255, 100, 100)), (bx + 445, by + 215))
                
                hp_ratio = target_live_companion.hp / target_live_companion.max_hp
                pygame.draw.rect(screen, (60, 20, 20), (bx + 445, by + 238, 240, 10))
                pygame.draw.rect(screen, (255, 50, 50), (bx + 445, by + 238, int(240 * hp_ratio), 10))
            else:
                screen.blit(font.render("狀態: 未實體化上陣", True, (150, 150, 150)), (bx + 445, by + 185))

            btn_color = (0, 180, 100) if btn_rect.collidepoint(m_pos_x, m_pos_y) else (0, 120, 70)
            pygame.draw.rect(screen, btn_color, btn_rect)
            pygame.draw.rect(screen, (255, 255, 255), btn_rect, 1)
            btn_text = title_font.render("部署生成此傳奇英靈", True, (255, 255, 255))
            screen.blit(btn_text, (btn_rect.centerx - btn_text.get_width()//2, btn_rect.centery - btn_text.get_height()//2))

        # 底部提示條
        pygame.draw.rect(screen, (20, 20, 30), (0, 565, 800, 35))
        guide_txt = font.render("自動掛機 OFF 時可用 WASD / 方向鍵 控制主角 | 面板開啟時點右鍵指派英靈", True, (0, 255, 220))
        screen.blit(guide_txt, (400 - guide_txt.get_width()//2, 573))

        pygame.display.flip()

if __name__ == "__main__":
    main()