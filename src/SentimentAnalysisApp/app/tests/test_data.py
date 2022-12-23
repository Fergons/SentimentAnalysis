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
        "language": "czech",
        "text": "Fast paced rogue-like RPG/Settlement building game\n\nWithout exploring all locations, main quest line and 100 % achievements sums up to 12 hours of game time.\n\nFirst hour you try to farm resources to build settlement and after you recruit your first follower (mage) you annihilate most of the foes. That means you find OP loot pretty fast and then it's only about quest doing.\n\nAchievements pop only when you save and quit game. Strength ramping of hero could be much slower but otherwise fine game.\n\n7/10",
        "summary": None,
        "score": None,
        "helpful_score": "0",
        "good": None,
        "bad": None,
        "voted_up": True,
        "created_at": "2022-05-08 19:27:44.000000 +00:00",
        "updated_at": None,
        "processed_at": None,
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
        "processed_at": None,
        "aspect_sum_polarity": None,
        "playtime_at_review": 4696
    }
]

TEST_REVIEWER = [
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

ALL_DATA = [
    TEST_SOURCE,
    TEST_CATEGORY,
    TEST_GAME,
    TEST_REVIEW,
    TEST_REVIEWER,
    TEST_GAME_CATEGORY,
    TEST_GAME_SOURCE
]
