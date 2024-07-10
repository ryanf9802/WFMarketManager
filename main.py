import pywmapi as wm
import logging
from util.ref.ref import updateRefs
import util.syndicate_specific as syn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output.log', mode='w'),
    ]
)
logger = logging.getLogger(__name__)

session = wm.auth.signin('ryanf9802@gmail.com', 'Coppernotice0101')

def main(updateReferences=True):
    if updateReferences:
        updateRefs()

if __name__ == "__main__":
    main()
