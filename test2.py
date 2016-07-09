
import logging


def main():
    
    
    logging.basicConfig(filename='example.log',level=logging.WARN)
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')

if __name__ == "__main__": main()