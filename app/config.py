import logging
import sys
from pathlib import Path

# लॉग्स स्टोर करने के लिए फोल्डर बनाना
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "matex_app.log"

# लॉगिंग कॉन्फ़िगरेशन
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        # 1. फाइल में सेव करने के लिए
        logging.FileHandler(LOG_FILE),
        # 2. टर्मिनल/कंसोल पर देखने के लिए
        logging.StreamHandler(sys.stdout)
    ]
)

# एक 'Global Logger' बनाना
logger = logging.getLogger("MateX")

# टेस्ट मैसेज
logger.info("MateX Logging System Initialized Successfully")