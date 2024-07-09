from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz

BOT_TOKEN = env.str("BOT_TOKEN")  # Bot Token
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
DATA_BASE = env.str("DATA_BASE") # Data Baza


