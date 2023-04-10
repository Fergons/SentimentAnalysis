TEST_SOURCE = [
    {
        "id": 1,
        "name": "steam",
        "url": "https://store.steampowered.com/api",
        "user_reviews_url": "https://store.steampowered.com/appreviews",
        "critic_reviews_url": None,
        "game_detail_url": "https://store.steampowered.com/api/appdetails",
        "list_of_games_url": "https://api.steampowered.com/ISteamApps/GetAppList/v2",
        "reviewer_detail_url": None,
        "list_of_reviewers_url": None,
        "updated_at": None
    },
    {
        "id": 2,
        "name": "metacritic",
        "url": "https://metacritic.com",
        "user_reviews_url": "https://metacritic.com",
        "critic_reviews_url": None,
        "game_detail_url": "https://metacritic.com",
        "list_of_games_url": "https://metacritic.com",
        "reviewer_detail_url": None,
        "list_of_reviewers_url": None,
        "updated_at": None
    },
    {
        "id": 3,
        "name": "gamespot",
        "url": "https://www.gamespot.com/api/",
        "user_reviews_url": "https://www.gamespot.com/api/reviews/",
        "critic_reviews_url": None,
        "game_detail_url": "http://www.gamespot.com/api/games/",
        "list_of_games_url": "http://www.gamespot.com/api/games/",
        "reviewer_detail_url": None,
        "list_of_reviewers_url": None,
        "updated_at": None
    },
    {
        "id": 4,
        "name": "doupe",
        "url": "https://doupe.zive.cz",
        "user_reviews_url": "https://doupe.zive.cz/recenze/",
        "critic_reviews_url": "https://doupe.zive.cz/recenze/",
        "game_detail_url": None,
        "list_of_games_url": None,
        "reviewer_detail_url": None,
        "list_of_reviewers_url": None,
        "updated_at": None
    }
    ,
    {
        "id": 99,
        "name": "test",
        "url": "http://localhost:8000",
        "user_reviews_url": "https://doupe.zive.cz/recenze/",
        "critic_reviews_url": "https://doupe.zive.cz/recenze/",
        "game_detail_url": None,
        "list_of_games_url": None,
        "reviewer_detail_url": None,
        "list_of_reviewers_url": None,
        "updated_at": None
    }

]
TEST_GAME = [
    {
        "id": 22,
        "name": "Undead Development",
        "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/682140/header.jpg?t=1610568361",
        "release_date": "2021-01-12 23:00:00.000000 +00:00",
        "updated_at": None
    },
    {
        "id": 278,
        "name": "Regions Of Ruin",
        "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/680360/header.jpg?t=1642197554",
        "release_date": "2018-02-04 23:00:00.000000 +00:00",
        "updated_at": "2022-12-16 10:37:49.653950 +00:00"
    },
    {
        "id": 281,
        "name": "OUTRIDERS",
        "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/680420/header.jpg?t=1657806851",
        "release_date": "2021-03-31 22:00:00.000000 +00:00",
        "updated_at": "2022-12-16 11:22:43.437274 +00:00"
    },
    {
        "id": 306,
        "name": "Swords & Souls: Neverseen",
        "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/679900/header.jpg?t=1664808504",
        "release_date": "2019-07-21 22:00:00.000000 +00:00",
        "updated_at": "2022-12-16 10:09:45.934795 +00:00"
    }
]

TEST_GAME_SOURCE = [
    {
        "id": 22,
        "game_id": 22,
        "source_id": 1,
        "source_game_id": "682140",
        "updated_at": None
    },
    {
        "id": 306,
        "game_id": 278,
        "source_id": 1,
        "source_game_id": "680360",
        "updated_at": None
    },
    {
        "id": 309,
        "game_id": 281,
        "source_id": 1,
        "source_game_id": "680420",
        "updated_at": None
    },
    {
        "id": 364,
        "game_id": 306,
        "source_id": 1,
        "source_game_id": "679900",
        "updated_at": None
    },
    {
        "id": 365,
        "game_id": 22,
        "source_id": 2,
        "source_game_id": "682232140",
        "updated_at": None
    },
    {
        "id": 366,
        "game_id": 281,
        "source_id": 2,
        "source_game_id": "623480420",
        "updated_at": None
    },
    {
        "id": 367,
        "game_id": 306,
        "source_id": 2,
        "source_game_id": "68230420",
        "updated_at": None
    },
]

TEST_CATEGORY = [
    {
        "id": 1,
        "name": "Single-player"
    },
    {
        "id": 2,
        "name": "Steam Cloud"
    },
    {
        "id": 3,
        "name": "Steam Trading Cards"
    },
    {
        "id": 4,
        "name": "Steam Achievements"
    },
    {
        "id": 5,
        "name": "Multi-player"
    },
    {
        "id": 6,
        "name": "Co-op"
    },
    {
        "id": 7,
        "name": "Online Co-op"
    },
    {
        "id": 8,
        "name": "Captions available"
    },
    {
        "id": 9,
        "name": "Stats"
    },
    {
        "id": 10,
        "name": "Steam Leaderboards"
    },
    {
        "id": 11,
        "name": "PvP"
    },
    {
        "id": 12,
        "name": "Online PvP"
    },
    {
        "id": 13,
        "name": "Cross-Platform Multiplayer"
    },
    {
        "id": 14,
        "name": "Shared/Split Screen PvP"
    },
    {
        "id": 15,
        "name": "Shared/Split Screen"
    },
    {
        "id": 16,
        "name": "Partial Controller Support"
    },
    {
        "id": 17,
        "name": "Remote Play Together"
    },
    {
        "id": 18,
        "name": "Full controller support"
    },
    {
        "id": 19,
        "name": "MMO"
    },
    {
        "id": 20,
        "name": "In-App Purchases"
    },
    {
        "id": 21,
        "name": "Steam Workshop"
    },
    {
        "id": 22,
        "name": "Includes level editor"
    },
    {
        "id": 23,
        "name": "Shared/Split Screen Co-op"
    },
    {
        "id": 24,
        "name": "Remote Play on TV"
    },
    {
        "id": 25,
        "name": "Commentary available"
    },
    {
        "id": 26,
        "name": "LAN PvP"
    },
    {
        "id": 27,
        "name": "LAN Co-op"
    },
    {
        "id": 28,
        "name": "Downloadable Content"
    },
    {
        "id": 29,
        "name": "Remote Play on Tablet"
    },
    {
        "id": 30,
        "name": "Remote Play on Phone"
    },
    {
        "id": 31,
        "name": "Action"
    },
    {
        "id": 32,
        "name": "Adventure"
    },
    {
        "id": 33,
        "name": "RPG"
    },
    {
        "id": 34,
        "name": "Indie"
    },
    {
        "id": 35,
        "name": "Casual"
    },
    {
        "id": 36,
        "name": "Simulation"
    },
    {
        "id": 37,
        "name": "Sports"
    },
    {
        "id": 38,
        "name": "Early Access"
    },
    {
        "id": 39,
        "name": "Strategy"
    },
    {
        "id": 40,
        "name": "Racing"
    },
    {
        "id": 41,
        "name": "Massively Multiplayer"
    },
    {
        "id": 42,
        "name": "Free to Play"
    },
    {
        "id": 43,
        "name": "Audio Production"
    },
    {
        "id": 44,
        "name": "Education"
    },
    {
        "id": 45,
        "name": "Utilities"
    },
    {
        "id": 46,
        "name": "Tracked Controller Support"
    },
    {
        "id": 47,
        "name": "Steam Turn Notifications"
    },
    {
        "id": 48,
        "name": "Animation & Modeling"
    },
    {
        "id": 49,
        "name": "Design & Illustration"
    },
    {
        "id": 50,
        "name": "Software Training"
    },
    {
        "id": 51,
        "name": "Video Production"
    },
    {
        "id": 52,
        "name": "Web Publishing"
    },
    {
        "id": 53,
        "name": "Photo Editing"
    },
    {
        "id": 54,
        "name": "Game Development"
    },
    {
        "id": 55,
        "name": "Includes Source SDK"
    },
    {
        "id": 56,
        "name": "Sexual Content"
    },
    {
        "id": 57,
        "name": "Gore"
    },
    {
        "id": 58,
        "name": "Valve Anti-Cheat enabled"
    },
    {
        "id": 59,
        "name": "VR Support"
    },
    {
        "id": 60,
        "name": "SteamVR Collectibles"
    },
    {
        "id": 61,
        "name": "Violent"
    },
    {
        "id": 62,
        "name": "Mods"
    }
]

TEST_GAME_CATEGORY = [
    {
        "id": 47,
        "game_id": 22,
        "category_id": 1
    },
    {
        "id": 715,
        "game_id": 278,
        "category_id": 1
    },
    {
        "id": 716,
        "game_id": 278,
        "category_id": 4
    },
    {
        "id": 717,
        "game_id": 278,
        "category_id": 3
    },
    {
        "id": 718,
        "game_id": 278,
        "category_id": 16
    },
    {
        "id": 719,
        "game_id": 278,
        "category_id": 2
    },
    {
        "id": 724,
        "game_id": 281,
        "category_id": 1
    },
    {
        "id": 725,
        "game_id": 281,
        "category_id": 5
    },
    {
        "id": 726,
        "game_id": 281,
        "category_id": 6
    },
    {
        "id": 727,
        "game_id": 281,
        "category_id": 7
    },
    {
        "id": 728,
        "game_id": 281,
        "category_id": 13
    },
    {
        "id": 729,
        "game_id": 281,
        "category_id": 4
    },
    {
        "id": 730,
        "game_id": 281,
        "category_id": 18
    },
    {
        "id": 731,
        "game_id": 281,
        "category_id": 3
    },
    {
        "id": 798,
        "game_id": 306,
        "category_id": 1
    },
    {
        "id": 799,
        "game_id": 306,
        "category_id": 4
    },
    {
        "id": 800,
        "game_id": 306,
        "category_id": 3
    },
    {
        "id": 801,
        "game_id": 306,
        "category_id": 10
    }
]

TEST_REVIEW = [
    {
        "id": 776,
        "source_review_id": "123358484",
        "source_reviewer_id": None,
        "game_id": 278,
        "reviewer_id": 6,
        "source_id": 1,
        "language": "czech",
        "text": "Tato hra mě moc bavila a můžu jí vřele doporučit.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-10-04 19:34:33.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 1154
    },
    {
        "id": 777,
        "source_review_id": "115171666",
        "source_reviewer_id": None,
        "game_id": 278,
        "reviewer_id": 7,
        "source_id": 1,
        "language": "english",
        "text": "Fast paced rogue-like RPG/Settlement building game\n\nWithout exploring all locations, main quest line and 100 % achievements sums up to 12 hours of game time.\n\nFirst hour you try to farm resources to build settlement and after you recruit your first follower (mage) you annihilate most of the foes. That means you find OP loot pretty fast and then it's only about quest doing.\n\nAchievements pop only when you save and quit game. Strength ramping of hero could be much slower but otherwise fine game.\n\n7/10",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-05-08 19:27:44.000000 +00:00",
        "updated_at": None,
        "processed_at": "2023-02-11 00:00:00.000000 +00:00",
        "aspect_sum_polarity": None,
        "playtime_at_review": 727
    },
    {
        "id": 779,
        "source_review_id": "84560220",
        "source_reviewer_id": None,
        "game_id": 278,
        "reviewer_id": 9,
        "source_id": 1,
        "language": "czech",
        "text": "Skvělá hra, jednoduché ovládání, dobrý resource management, dobrý combat. \nTrochu mě štvalo hledat místa, které mají tu surovinu, kterou zrovna potřebuji. Hrál jsem crit-build, takže bylo krásné vidět těžkou jednotku, která dostala jednou ránou 200K dmg. \nLoot padá pořád a pořád je co zabíjet.\n\n",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2021-01-12 16:29:25.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 642
    },
    {
        "id": 1384,
        "source_review_id": "62524014",
        "source_reviewer_id": None,
        "game_id": 306,
        "reviewer_id": 606,
        "source_id": 1,
        "language": "czech",
        "text": "nelíbilo se mi že  toho nebylo více a líbilo se mi že je to dost propracovaný\n\n\n\n\n¨\n",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2020-01-27 17:18:13.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 817
    },
    {
        "id": 1359,
        "source_review_id": "77888325",
        "source_reviewer_id": None,
        "game_id": 306,
        "reviewer_id": 582,
        "source_id": 1,
        "language": "czech",
        "text": "Great!!!",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2020-10-20 20:24:54.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 663
    },
    {
        "id": 1301,
        "source_review_id": "96694081",
        "source_reviewer_id": None,
        "game_id": 306,
        "reviewer_id": 524,
        "source_id": 1,
        "language": "czech",
        "text": "Hra je velmi zábavná a nikdy neomrzí.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2021-07-31 14:22:48.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 1494
    },
    {
        "id": 1302,
        "source_review_id": "96418045",
        "source_reviewer_id": None,
        "game_id": 306,
        "reviewer_id": 525,
        "source_id": 1,
        "language": "czech",
        "text": "good game",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2021-07-26 18:25:52.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 6212
    },
    {
        "id": 1141,
        "source_review_id": "90028864",
        "source_reviewer_id": None,
        "game_id": 281,
        "reviewer_id": 366,
        "source_id": 1,
        "language": "czech",
        "text": "Im frustrated and I cant stop playing. Help",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2021-04-09 21:38:38.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 809,
    },
    {
        "id": 1053,
        "source_review_id": "102411613",
        "source_reviewer_id": None,
        "game_id": 281,
        "reviewer_id": 280,
        "source_id": 1,
        "language": "czech",
        "text": "klasická loot&shooter v přijemném scifi prostředí. Zajimavý endgame , slušelo by tomu více map a legendarních setů pro lepší variabilitu.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2021-11-07 23:25:24.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 2745
    },
    {
        "id": 1246,
        "source_review_id": "121564688",
        "source_reviewer_id": None,
        "game_id": 306,
        "reviewer_id": 470,
        "source_id": 1,
        "language": "czech",
        "text": "jo",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-09-01 09:53:25.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 417
    },
    {
        "id": 1006,
        "source_review_id": "125421684",
        "source_reviewer_id": None,
        "game_id": 281,
        "reviewer_id": 233,
        "source_id": 1,
        "language": "czech",
        "text": "Hra je úplny výsmech hráčom. Po dohratí kampane mám kupovať predražené dlc, ktoré trvá cca. 3 hodiny ale stoji 40 ečok? A to aby som mohol vylepšovať ďalej svoju postavu. Samotná hra ma neskutočne veľa chýb od divne zostrihaných story videí  až po game dizajn.  \nmínus\n- cena samotnej hry\n- cena DLC a hráči si musia kúpiť DLC ak chcú hrať end game (ak nekúpia budú slabší ako ostatný hrači)\n- bedne s muníciou sú na pi... rozložené po mape \n- story videá sú divne nastrihané \nplus\n- módy na vybavení sa dajú meniť\n-akokoľvek rozmýšlam viac plusov nieje",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": False,
        "created_at": "2022-11-13 17:10:08.000000 +00:00",
        "updated_at": None,
        "processed_at": "2023-02-11 00:00:00.000000 +00:00",
        "aspect_sum_polarity": None,
        "playtime_at_review": 4696
    },
    {
        "id": 2345,
        "source_review_id": "347612879",
        "source_reviewer_id": None,
        "game_id": 22,
        "reviewer_id": 6,
        "source_id": 1,
        "language": "czech",
        "text": "Tato hra mě opravdu zklamala. Očekával jsem více obsahu a lepší hratelnost. Nedoporučuji.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": False,
        "created_at": "2022-12-19 18:34:12.123456 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 25
    },
    {
        "id": 5678,
        "source_review_id": "983465213",
        "source_reviewer_id": None,
        "game_id": 278,
        "reviewer_id": 7,
        "source_id": 1,
        "language": "czech",
        "text": "Tuto hru jsem si užil. Grafika je skvělá a hratelnost je návyková. Doporučuji.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-12-22 09:12:34.567890 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 100
    },
    {
        "id": 9012,
        "source_review_id": "287345671",
        "source_reviewer_id": None,
        "game_id": 281,
        "reviewer_id": 9,
        "source_id": 1,
        "language": "czech",
        "text": "Tato hra je jednoduchá a zábavná. Určitě si ji zahrajte, pokud máte rádi jednoduché hry.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-12-25 16:42:56.789012 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 10
    },
    {
        "id": 1234,
        "source_review_id": "753914268",
        "source_reviewer_id": None,
        "game_id": 306,
        "reviewer_id": 233,
        "source_id": 1,
        "language": "czech",
        "text": "Tato hra mě překvapila. Byla to skvělá zábava a určitě si ji zahraju znovu.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-12-25 16:00:56.789012 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 10
    },
    {
        "id": 5673,
        "source_review_id": "984765213",
        "source_reviewer_id": None,
        "game_id": 278,
        "reviewer_id": 7,
        "source_id": 1,
        "language": "czech",
        "text": "Tuto hru jsem si užil. Grafika je skvělá a hratelnost je návyková. Doporučuji.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-12-22 09:12:34.567890 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 100
    },
    # create more reviews here with random integer as "id", random datetime for "created_at", and random "review_source_id" as integer string and "reviewer_id" from ids in REVIEWERS
    # and "game_id" from ids in GAMES
    # and "source_id" from ids in SOURCES
    # and use "czech" for "language"
    # and use random integer for "playtime_at_review"
    # and use random game review in czech language for "text" using max 250 characters
    # and use random integer as string for "helpful_score"

    {
        "id": 43,
        "source_review_id": "126556789",
        "source_reviewer_id": None,
        "game_id": 278,
        "reviewer_id": 9,
        "source_id": 1,
        "language": "czech",
        "text": "Tato hra mě překvapila. Byla to skvělá zábava a určitě si ji zahraju znovu.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-12-25 16:00:56.789012 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 10
    },
    {
        "id": 34,  # random integer
        "source_review_id": "123456789",  # random integer as string
        "source_reviewer_id": None,
        "game_id": 306,  # id from GAMES
        "reviewer_id": 7,
        "source_id": 1,
        "language": "czech",
        "text": "Tato hra mě překvapila. Byla to skvělá zábava a určitě si ji zahraju znovu.",  # random game review
        "summary": None,
        "score": None,
        "helpful_score": "0",  # random integer as string
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-12-23 16:00:56.789012 +00:00",  # random datetime
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 1043  # random integer
    },
    {
        "id": 35,  # random integer
        "source_review_id": "123766789",  # random integer as string
        "source_reviewer_id": None,
        "game_id": 306,  # random id from GAMES
        "reviewer_id": 7,  # random id from REVIEWERS
        "source_id": 1,  # random id from SOURCES
        "language": "czech",
        "text": "Tato hra mě překvapila. Super gameplay a grafika.",  # random game review
        "summary": None,
        "score": None,
        "helpful_score": "0",  # random integer as string
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-09-23 16:00:56.789012 +00:00",  # random datetime
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 133  # random integer
    },
    {
        "id": 36,  # random integer
        "source_review_id": "82336789",  # random integer as string
        "source_reviewer_id": None,
        "game_id": 22,  # random id from (22, 278, 306, 281)
        "reviewer_id": 7,  # random id from (6, 7, 9, 233)
        "source_id": 1,
        "language": "czech",
        "text": "Super cena za takovou hru.",  # random game review
        "summary": None,
        "score": None,
        "helpful_score": "0",  # random integer as string
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-12-23 13:00:56.789012 +00:00",  # random datetime
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 143  # random integer
    },
    {
        "id": 2235,
        "source_review_id": "95861765",
        "source_reviewer_id": None,
        "game_id": 22,
        "reviewer_id": 6,
        "source_id": 1,
        "language": "czech",
        "text": "Hra je zábavná, ale na můj vkus příliš krátká.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-12-28 13:26:19.548302 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 150
    },
    {
        "id": 3872,
        "source_review_id": "746135861",
        "source_reviewer_id": None,
        "game_id": 278,
        "reviewer_id": 7,
        "source_id": 1,
        "language": "czech",
        "text": "Nemůžu si vynachválit grafiku a hudební doprovod, ale hratelnost zůstává slabým místem této hry.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": False,
        "created_at": "2022-12-19 09:45:32.846701 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 250
    },
    {
        "id": 4927,
        "source_review_id": "52967817",
        "source_reviewer_id": None,
        "game_id": 306,
        "reviewer_id": 9,
        "source_id": 1,
        "language": "czech",
        "text": "Velmi povedená hra s nádhernou grafikou a bohatou hratelností.",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-12-09 20:31:59.272080 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 500
    },
    {
        "id": 3874,
        "source_review_id": "690245123",
        "source_reviewer_id": "76561198873244567",
        "game_id": 22,
        "reviewer_id": 456,
        "source_id": 2,
        "language": "czech",
        "text": "Tato hra mě zklamala. Grafika a hudební doprovod jsou sice dobré, ale hratelnost je příliš repetitivní a brzy mě přestala bavit.",
        "summary": "Zklamání",
        "score": "5",
        "helpful_score": "1",
        "good": "Dobrá grafika a hudební doprovod",
        "bad": "Příliš repetitivní hratelnost",
        "voted_up": False,
        "created_at": "2023-02-24 18:30:10.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": "0.5",
        "playtime_at_review": 20
    },
    {
        "id": 3833,
        "source_review_id": "892105623",
        "source_reviewer_id": "76561198912495123",
        "game_id": 306,
        "reviewer_id": 123,
        "source_id": 2,
        "language": "czech",
        "text": "Tato hra je naprosto úžasná! Mám ji už několik týdnů a stále se mi v ní nechce přestat hrát. Grafika je skvělá a hudební doprovod dokonale ladí s atmosférou. Hratelnost je velmi zábavná a nikdy se mi nezdála nudná.",
        "summary": "Naprosto úžasná hra",
        "score": "10",
        "helpful_score": "5",
        "good": "Skvělá grafika, dokonalý hudební doprovod, velmi zábavná hratelnost",
        "bad": None,
        "voted_up": True,
        "created_at": "2023-02-25 14:15:30.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": "1.0",
        "playtime_at_review": 50
    },
    {
        "id": 891,
        "source_review_id": "467831496",
        "source_reviewer_id": None,
        "game_id": 306,
        "reviewer_id": 123,
        "source_id": 2,
        "language": "english",
        "text": "This game is a lot of fun and has some really cool mechanics. However, it can be frustrating at times due to bugs and glitches.",
        "summary": "Fun game with some issues",
        "score": "7.5",
        "helpful_score": "4",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-02-12 16:32:15.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": "0.5",
        "playtime_at_review": 35
    },

    {
        "id": 892,
        "source_review_id": "938166173",
        "source_reviewer_id": None,
        "game_id": 22,
        "reviewer_id": 123,
        "source_id": 2,
        "language": "english",
        "text": "I really enjoyed playing this game. The graphics and sound are top-notch, and the story kept me engaged from start to finish.",
        "summary": "Great game!",
        "score": "9.0",
        "helpful_score": "10",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-04-05 10:15:00.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": "1.0",
        "playtime_at_review": 40
    },
    {
        "id": 893,
        "source_review_id": "381609421",
        "source_reviewer_id": None,
        "game_id": 306,
        "reviewer_id": 456,
        "source_id": 2,
        "language": "english",
        "text": "I was really looking forward to playing this game, but unfortunately it was a huge disappointment. The graphics are mediocre at best, and the gameplay is just plain boring.",
        "summary": "Not worth your time",
        "score": "3.0",
        "helpful_score": "2",
        "good": None,
        "bad": None,
        "voted_up": False,
        "created_at": "2022-05-20 09:45:00.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": "-0.5",
        "playtime_at_review": 20
    },

    {
        "id": 894,
        "source_review_id": "139674971",
        "source_reviewer_id": None,
        "game_id": 281,
        "reviewer_id": 456,
        "source_id": 2,
        "language": "english",
        "text": "I wasn't sure what to expect from this game, but I ended up loving it! The gameplay is addictive and the graphics are beautiful.",
        "summary": "Surprisingly great",
        "score": "8.5",
        "helpful_score": "8",
        "good": None,
        "bad": None,
        "voted_up": False,
        "created_at": "2022-05-20 09:45:00.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
        "aspect_sum_polarity": "-0.5",
        "playtime_at_review": 31
    }

]

TEST_REVIEWER = [
    {
        "id": 456,
        "name": "David Kim",
        "source_reviewer_id": "76561198873244567",
        "source_id": 2,
        "updated_at": None,
        "num_games_owned": 15,
        "num_reviews": 8
    },
    {
        "id": 123,
        "name": "Sarah Lee",
        "source_reviewer_id": "76561198912495123",
        "source_id": 2,
        "updated_at": None,
        "num_games_owned": 87,
        "num_reviews": 42
    },

    {
        "id": 6,
        "name": None,
        "source_reviewer_id": "76561198079043053",
        "source_id": 1,
        "updated_at": None,
        "num_games_owned": 211,
        "num_reviews": 4
    },
    {
        "id": 7,
        "name": None,
        "source_reviewer_id": "76561198038910520",
        "source_id": 1,
        "updated_at": None,
        "num_games_owned": 1515,
        "num_reviews": 16
    },
    {
        "id": 9,
        "name": None,
        "source_reviewer_id": "76561198033734206",
        "source_id": 1,
        "updated_at": None,
        "num_games_owned": 144,
        "num_reviews": 1
    },
    {
        "id": 233,
        "name": None,
        "source_reviewer_id": "76561198043962347",
        "source_id": 1,
        "updated_at": None,
        "num_games_owned": 117,
        "num_reviews": 6
    },
    {
        "id": 280,
        "name": None,
        "source_reviewer_id": "76561198883791239",
        "source_id": 1,
        "updated_at": None,
        "num_games_owned": 46,
        "num_reviews": 6
    },
    {
        "id": 366,
        "name": None,
        "source_reviewer_id": "76561198262666479",
        "source_id": 1,
        "updated_at": None,
        "num_games_owned": 93,
        "num_reviews": 6
    },
    {
        "id": 470,
        "name": None,
        "source_reviewer_id": "76561198384342990",
        "source_id": 1,
        "updated_at": None,
        "num_games_owned": 76,
        "num_reviews": 7
    },
    {
        "id": 524,
        "name": None,
        "source_reviewer_id": "76561199132207837",
        "source_id": 1,
        "updated_at": None,
        "num_games_owned": 7,
        "num_reviews": 2
    },
    {
        "id": 525,
        "name": None,
        "source_reviewer_id": "76561198843617189",
        "source_id": 1,
        "updated_at": None,
        "num_games_owned": 39,
        "num_reviews": 18
    },
    {
        "id": 582,
        "name": None,
        "source_reviewer_id": "76561198905130354",
        "source_id": 1,
        "updated_at": None,
        "num_games_owned": 25,
        "num_reviews": 5
    },
    {
        "id": 606,
        "name": None,
        "source_reviewer_id": "76561198823606578",
        "source_id": 1,
        "updated_at": None,
        "num_games_owned": 25,
        "num_reviews": 2
    }
]

TEST_ASPECTS = [
    {
        "id": 1,
        "review_id": 777,
        "term": "game time",
        "polarity": "neutral",
        "category": "overall",
        "opinion": "0.9",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 2,
        "review_id": 777,
        "term": "rogue-like RPG/Settlement building game",
        "polarity": "positive",
        "category": "gameplay",
        "opinion": "0.9",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 3,
        "review_id": 777,
        "term": "farm resources",
        "polarity": "neutral",
        "category": "gameplay",
        "opinion": "0.9",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 4,
        "review_id": 777,
        "term": "settlement",
        "polarity": "positive",
        "category": "gameplay",
        "opinion": "0.9",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 5,
        "review_id": 777,
        "term": "foes",
        "polarity": "positive",
        "category": "gameplay",
        "opinion": "0.9",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 6,
        "review_id": 777,
        "term": "OP loot",
        "polarity": "positive",
        "category": "gameplay",
        "opinion": "0.9",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 7,
        "review_id": 777,
        "term": "quest doing",
        "polarity": "positive",
        "category": "gameplay",
        "opinion": "0.9",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 18,
        "review_id": 777,
        "term": "achievements",
        "polarity": "neutral",
        "category": "gameplay",
        "opinion": "0.9",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 8,
        "review_id": 777,
        "term": "Strength ramping of hero",
        "polarity": "neutral",
        "category": "gameplay",
        "opinion": "0.9",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 9,
        "review_id": 777,
        "term": "gameplay",
        "polarity": "positive",
        "category": "gameplay",
        "opinion": "0.9",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 1234,
        "review_id": 1006,
        "term": "cena samotnej hry",
        "polarity": "negative",
        "category": "price",
        "opinion": "0.88",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 232423,
        "review_id": 1006,
        "term": "cena DLC",
        "polarity": "negative",
        "category": "price",
        "opinion": "0.88",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 3324,
        "review_id": 1006,
        "term": "hráči si musia kúpiť DLC",
        "polarity": "negative",
        "category": "price",
        "opinion": "0.88",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    },
    {
        "id": 4342,
        "review_id": 1006,
        "term": "divne zostrihaných story videí",
        "polarity": "negative",
        "category": "audio_visuals",
        "opinion": "0.88",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00",
    },
    {
        "id": 325,
        "review_id": 1006,
        "term": "game dizajn",
        "polarity": "negative",
        "category": "gameplay",
        "opinion": "0.88",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00",
    },
    {
        "id": 346,
        "review_id": 1006,
        "term": "bedne s muníciou",
        "polarity": "negative",
        "category": "gameplay",
        "opinion": "0.88",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00",
    },
    {
        "id": 337,
        "review_id": 1006,
        "term": "story videá",
        "polarity": "negative",
        "category": "audio_visuals",
        "opinion": "0.88",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00",
    },
    {
        "id": 38,
        "review_id": 1006,
        "term": "módy na vybavení",
        "polarity": "positive",
        "category": "gameplay",
        "opinion": "0.88",
        "model_id": "mdebertav3_74ATEPC",
        "updated_at": "2023-02-11 00:00:00.000000 +00:00"
    }
]

ALL_DATA = [
    TEST_SOURCE,
    TEST_CATEGORY,
    TEST_GAME,
    TEST_REVIEW,
    TEST_REVIEWER,
    TEST_GAME_CATEGORY,
    TEST_GAME_SOURCE,
    TEST_ASPECTS
]
