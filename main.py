import asyncio
import random
import os
import json
import aiosqlite
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

# ================= КОНФИГ =================
BOT_TOKEN = "9059779756:AAG-2MF3Km76UeqIRYUmI0ov15Lng_XBDYg" # ОБЯЗАТЕЛЬНО ПОМЕНЯЙ!
ADMIN_ID = 2092773964
DB_PATH = "game.db"

# ================= ДАННЫЕ БРЕЙНРОТОВ (Цены 1 в 1 со скринов) =================
BRAINROTS = [
  {"id": "hydra_dragon", "name": "Hydra Dragon Cannon", "price": 1281},
  {"id": "tirilikalika", "name": "Tirilikalika Tirilikala", "price": 1318},
  {"id": "bloodmoon_hammer", "name": "Bloodmoon Hammer", "price": 1322},
  {"id": "moby_bros", "name": "Moby Bros", "price": 1685},
  {"id": "hydra_bunny", "name": "Hydra Bunny", "price": 1809},
  {"id": "ginger_geratoni", "name": "Ginger Geratoni", "price": 2064},
  {"id": "fishino_clownino", "name": "Fishino Clownino", "price": 2104},
  {"id": "kraken", "name": "Kraken", "price": 2132},
  {"id": "digi_narwhal", "name": "Digi Narwhal", "price": 2246},
  {"id": "la_supreme_combo", "name": "La Supreme Combo", "price": 2420},
  {"id": "kalika_bros", "name": "Kalika Bros", "price": 3644},
  {"id": "dragon_aquanil", "name": "Dragon Aquanil", "price": 3887},
  {"id": "antonio", "name": "Antonio", "price": 4849},
  {"id": "dragon_gingerini", "name": "Dragon Gingerini", "price": 5161},
  {"id": "griffin", "name": "Griffin", "price": 6623},
  {"id": "love_love_bear", "name": "Love Love Bear", "price": 7074},
  {"id": "arcadragon", "name": "Arcadragon", "price": 9408},
  {"id": "elefanto_frigo", "name": "Elefanto Frigo", "price": 9562},
  {"id": "smore_serat", "name": "Smore Serat", "price": 399},
  {"id": "rubiko_and_kubiko", "name": "Rubiko and Kubiko", "price": 415},
  {"id": "los_hackers", "name": "Los Hackers", "price": 420},
  {"id": "foxini_lanternini", "name": "Foxini Lanternini", "price": 426},
  {"id": "los_secret_combo", "name": "Los Secret Combo", "price": 440},
  {"id": "venusplno", "name": "Venusplno", "price": 512},
  {"id": "ketupat_bros", "name": "Ketupat Bros", "price": 513},
  {"id": "bumbatron", "name": "Bumbatron", "price": 529},
  {"id": "rosey_and_teddy", "name": "Rosey and Teddy", "price": 552},
  {"id": "sammyni_cakini", "name": "Sammyni Cakini", "price": 572},
  {"id": "la_casa_boo", "name": "La Casa Boo", "price": 579},
  {"id": "rainbow_hammer", "name": "Rainbow Hammer", "price": 655},
  {"id": "sammyni_trackini", "name": "Sammyni Trackini", "price": 661},
  {"id": "bunny_and_eggy", "name": "Bunny and Eggy", "price": 906},
  {"id": "dragon_cannon", "name": "Dragon Cannon", "price": 1022},
  {"id": "pancake_and_syrup", "name": "Pancake and Syrup", "price": 1060},
  {"id": "grabatron", "name": "Grabatron", "price": 1182},
  {"id": "jelly_moby", "name": "Jelly Moby", "price": 1211},
  {"id": "festive_67", "name": "Festive 67", "price": 207},
  {"id": "fragola_la_la", "name": "Fragola La La", "price": 212},
  {"id": "la_fuse_machine", "name": "La Fuse Machine", "price": 220},
  {"id": "no_my_examine", "name": "No My Examine", "price": 221},
  {"id": "dug_dug_dug", "name": "Dug dug dug", "price": 237},
  {"id": "fortunu_and_cash", "name": "Fortunu and Cash", "price": 242},
  {"id": "cangurato_gelato", "name": "Cangurato Gelato", "price": 255},
  {"id": "cloverat_clapat", "name": "Cloverat Clapat", "price": 258},
  {"id": "cayiusaurus", "name": "Cayiusaurus", "price": 267},
  {"id": "hopilikalika", "name": "Hopilikalika Hopilli", "price": 281},
  {"id": "la_breakfast_combo", "name": "La Breakfast Combo", "price": 287},
  {"id": "los_tacoritas", "name": "Los Tacoritas", "price": 290},
  {"id": "rico_dinero", "name": "Rico Dinero", "price": 308},
  {"id": "duggy_bros", "name": "Duggy Bros", "price": 340},
  {"id": "los_sekolahs", "name": "Los Sekolahs", "price": 342},
  {"id": "guest_666", "name": "Guest 666", "price": 353},
  {"id": "los_admins", "name": "Los Admins", "price": 389},
  {"id": "examen_bros", "name": "Examen Bros", "price": 393},
  {"id": "jolly_jolly_sahur", "name": "Jolly Jolly Sahur", "price": 139},
  {"id": "rosetti_tualetti", "name": "Rosetti Tualetti", "price": 140},
  {"id": "money_money_rel", "name": "Money Money Rel", "price": 140},
  {"id": "swaggy_bros", "name": "Swaggy Bros", "price": 150},
  {"id": "spooky_and_pump", "name": "Spooky and Pump", "price": 153},
  {"id": "boppin_bunny", "name": "Boppin Bunny", "price": 160},
  {"id": "money_money_bros", "name": "Money Money Bros", "price": 162},
  {"id": "cerberus", "name": "Cerberus", "price": 163},
  {"id": "la_ginger_sekolah", "name": "La Ginger Sekolah", "price": 164},
  {"id": "chipso_and_queso", "name": "Chipso and Queso", "price": 166},
  {"id": "chillin_chili", "name": "Chillin Chili", "price": 171},
  {"id": "trenostruzo", "name": "Trenostruzo Turb", "price": 180},
  {"id": "lovin_rose", "name": "Lovin Rose", "price": 181},
  {"id": "reinlto_sleightto", "name": "Reinlto Sleightto", "price": 185},
  {"id": "yetimatic", "name": "Yetimatic", "price": 192},
  {"id": "gym_bros", "name": "Gym Bros", "price": 199},
  {"id": "queen_bee", "name": "Queen Bee", "price": 199},
  {"id": "los_amigos", "name": "Los Amigos", "price": 201},
  {"id": "las_sis", "name": "Las Sis", "price": 99},
  {"id": "burguro_and_fryuro", "name": "Burguro And Fryuro", "price": 109},
  {"id": "la_food_comb", "name": "La Food Combination", "price": 109},
  {"id": "capitano_america", "name": "Capitano America", "price": 109},
  {"id": "swag_soda", "name": "Swag Soda", "price": 111},
  {"id": "steakini_fattini", "name": "Steakini Fattini", "price": 117},
  {"id": "gold_gold_gold", "name": "Gold Gold Gold", "price": 122},
  {"id": "tralaledon", "name": "Tralaledon", "price": 122},
  {"id": "los_cupids", "name": "Los Cupids", "price": 126},
  {"id": "fragrama_and_ch", "name": "Fragrama and Ch", "price": 128},
  {"id": "globa_steppa", "name": "Globa Steppa", "price": 131},
  {"id": "los_hotspotsitos", "name": "Los Hotspotsitos", "price": 131},
  {"id": "la_taco_comb", "name": "La Taco Combination", "price": 132},
  {"id": "capitano_moby", "name": "Capitano Moby", "price": 134},
  {"id": "los_spaghettis", "name": "Los Spaghettis", "price": 135},
  {"id": "pop_pop_petalini", "name": "Pop Pop Petalini", "price": 136},
  {"id": "cooki_and_mikl", "name": "Cooki and Mikl", "price": 137},
  {"id": "tuff_toucan", "name": "Tuff Toucan", "price": 138},
  {"id": "phantom_slap", "name": "Phantom Slap", "price": 60},
  {"id": "la_jolly_grande", "name": "La Jolly Grande", "price": 69},
  {"id": "sammyni_fattini", "name": "Sammyni Fattini", "price": 74},
  {"id": "evilodon", "name": "Evilodon", "price": 75},
  {"id": "w_or_l", "name": "W or L", "price": 78},
  {"id": "lava_blaster", "name": "Lava Blaster", "price": 80},
  {"id": "los_tictacs", "name": "Los Tictacs", "price": 82},
  {"id": "los_sweethearts", "name": "Los Sweethearts", "price": 84},
  {"id": "john_doe", "name": "John Doe", "price": 84},
  {"id": "pizza_and_ranch", "name": "Pizza and Ranch", "price": 84},
  {"id": "los_jolly_comb", "name": "Los Jolly Combination", "price": 91},
  {"id": "popcuru_and_fizz", "name": "Popcuru and Fizz", "price": 92},
  {"id": "los_mariachis", "name": "Los Mariachis", "price": 92},
  {"id": "quackini_snackini", "name": "Quackini Snackini", "price": 93},
  {"id": "santas_sleigh", "name": "Santas Sleigh", "price": 93},
  {"id": "la_secret_comb", "name": "La Secret Combination", "price": 95},
  {"id": "celestial_pegasus", "name": "Celestial Pegasus", "price": 98},
  {"id": "scorpino_coaster", "name": "Scorpino Coaster", "price": 98},
  {"id": "waverider", "name": "Waverider", "price": 37},
  {"id": "witch_broom", "name": "Witch Broom", "price": 40},
  {"id": "blackhole_bomb", "name": "Blackhole Bomb", "price": 40},
  {"id": "mi_gatito", "name": "Mi Gatito", "price": 41},
  {"id": "camera_ramen", "name": "Camera Ramen", "price": 41},
  {"id": "ventollero", "name": "Ventollero Pavon", "price": 44},
  {"id": "yes_my_examine", "name": "Yes My Examine", "price": 44},
  {"id": "los_primos", "name": "Los Primos", "price": 45},
  {"id": "air_strike", "name": "Air Strike", "price": 45},
  {"id": "candy_sentry", "name": "Candy Sentry", "price": 46},
  {"id": "los_planitos", "name": "Los Planitos", "price": 49},
  {"id": "la_summer_grande", "name": "La Summer Grande", "price": 49},
  {"id": "honey_honey_bear", "name": "Honey Honey Bear", "price": 51},
  {"id": "garama_and_mad", "name": "Garama and Mad", "price": 54},
  {"id": "ketchuru_and_mu", "name": "Ketchuru and Mu", "price": 54},
  {"id": "quesadillo_vampiro", "name": "Quesadillo Vampiro", "price": 55},
  {"id": "cash_or_card", "name": "Cash or Card", "price": 56},
  {"id": "noodle_noodle", "name": "Noodle Noodle P", "price": 57},
  {"id": "esok_sekolah", "name": "Esok Sekolah", "price": 17},
  {"id": "agarini_la_palini", "name": "Agarini La Palini", "price": 23},
  {"id": "abyssaloco", "name": "Abyssaloco", "price": 23},
  {"id": "los_mobills", "name": "Los Mobills", "price": 24},
  {"id": "rainbow_slap", "name": "Rainbow Slap", "price": 24},
  {"id": "los_burritos", "name": "Los Burritos", "price": 25},
  {"id": "los_puggles", "name": "Los Puggles", "price": 29},
  {"id": "orcaledon", "name": "Orcaledon", "price": 30},
  {"id": "ketupat_kepat", "name": "Ketupat Kepat", "price": 30},
  {"id": "mietetelra", "name": "Mietetelra Bicicle", "price": 30},
  {"id": "los_candies", "name": "Los Candies", "price": 32},
  {"id": "demon_head", "name": "Demon Head", "price": 32},
  {"id": "lavadorito", "name": "Lavadorito Spinto", "price": 33},
  {"id": "crystal_slap", "name": "Crystal Slap", "price": 33},
  {"id": "ying_yang_lamp", "name": "Ying Yang Lamp", "price": 34},
  {"id": "bloodmoon_slap", "name": "Bloodmoon Slap", "price": 35},
  {"id": "cupid_wings", "name": "Cupid Wings", "price": 36},
  {"id": "los_tangclitos", "name": "Los Tangclitos", "price": 36},
  {"id": "los_trios", "name": "Los Trios", "price": 5},
  {"id": "sixty_seven", "name": "67", "price": 6},
  {"id": "spinny_hammy", "name": "Spinny Hammy", "price": 7},
  {"id": "arcadopus", "name": "Arcadopus", "price": 8},
  {"id": "candy_slap", "name": "Candy Slap", "price": 8},
  {"id": "los_noobinis", "name": "Los Noobinis", "price": 8},
  {"id": "tang_tang", "name": "Tang Tang Keleta", "price": 9},
  {"id": "la_grande", "name": "La Grande", "price": 10},
  {"id": "divine_slap", "name": "Divine Slap", "price": 10},
  {"id": "tictac_sahur", "name": "Tictac Sahur", "price": 13},
  {"id": "bacuru_and_egguru", "name": "Bacuru and Egguru", "price": 13},
  {"id": "los_67", "name": "Los 67", "price": 13},
  {"id": "cursed_slap", "name": "Cursed Slap", "price": 13},
  {"id": "ying_yang_slap", "name": "Ying Yang Slap", "price": 13},
  {"id": "los_combinasonas", "name": "Los Combinasonas", "price": 15},
  {"id": "money_puggy", "name": "Money Puggy", "price": 15},
  {"id": "lava_slap", "name": "Lava Slap", "price": 15},
  {"id": "nuclearo_dinosaur", "name": "Nuclearo Dinosaur", "price": 16}
]

# ================= ФУНКЦИИ =================

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 100000)")
        await db.commit()

async def get_balance(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row: return row[0]
            await db.execute("INSERT INTO users (user_id, balance) VALUES (?, 100000)", (user_id,))
            await db.commit()
            return 100000

async def update_balance(user_id, amount):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        await db.commit()

async def get_image(brainrot_name: str) -> str | None:
    safe_name = "".join(c for c in brainrot_name if c.isalnum() or c in " _-").replace(" ", "_")
    local_path = f"images/{safe_name}.png"
    if os.path.exists(local_path): return local_path
    
    wiki_url = "https://stealabrainrot.fandom.com/api.php"
    params = {"action": "query", "titles": brainrot_name, "prop": "pageimages", "format": "json", "pithumbsize": "500"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(wiki_url, params=params) as resp:
                data = await resp.json()
                pages = data.get("query", {}).get("pages", {})
                for page in pages.values():
                    if "thumbnail" in page:
                        img_url = page["thumbnail"]["source"]
                        async with session.get(img_url) as img_resp:
                            if img_resp.status == 200:
                                content = await img_resp.read()
                                os.makedirs("images", exist_ok=True)
                                with open(local_path, "wb") as f:
                                    f.write(content)
                                return local_path
    except Exception as e:
        print(f"Error fetching image: {e}")
    return None

# ================= БОТ =================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    balance = await get_balance(message.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Открыть кейс (100 ₽)", callback_data="open_case")],
        [InlineKeyboardButton(text="⬆️ Апгрейдер", callback_data="upgrade_menu")]
    ])
    await message.answer(f"👋 Добро пожаловать в SABgrader!\n\n💰 Твой баланс: {balance} ₽", reply_markup=kb)

@dp.callback_query(F.data == "open_case")
async def open_case(call: CallbackQuery):
    user_id = call.from_user.id
    balance = await get_balance(user_id)
    case_price = 100
    
    if balance < case_price:
        await call.answer("Недостаточно средств!", show_alert=True)
        return

    await update_balance(user_id, -case_price)
    await call.message.edit_text("🎰 Открываем кейс...")

    # Анимация прокрутки
    for _ in range(5):
        fake = random.choice(BRAINROTS)
        img_path = await get_image(fake["name"])
        try:
            if img_path:
                await call.message.edit_media(media=FSInputFile(img_path), caption=f"🎲 {fake['name']}...")
            else:
                await call.message.edit_text(f"🎲 {fake['name']}...")
        except:
            await call.message.edit_text(f"🎲 {fake['name']}...")
        await asyncio.sleep(0.2)

    # Выигрыш
    win = random.choice(BRAINROTS)
    img_path = await get_image(win["name"])
    text = f"🏆 Ты выиграл: **{win['name']}**!\n💰 Стоимость: {win['price']} ₽"
    
    try:
        if img_path:
            await call.message.edit_media(media=FSInputFile(img_path), caption=text, parse_mode="Markdown")
        else:
            await call.message.edit_text(text, parse_mode="Markdown")
    except:
        await call.message.edit_text(text, parse_mode="Markdown")

    # Звук (если есть)
    if os.path.exists("sounds/win.mp3"):
        try: await call.message.answer_audio(FSInputFile("sounds/win.mp3"))
        except: pass

@dp.callback_query(F.data == "upgrade_menu")
async def upgrade_menu(call: CallbackQuery):
    await call.answer("Здесь будет выбор предмета для апгрейда (доделаем позже)", show_alert=True)

async def main():
    await init_db()
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
