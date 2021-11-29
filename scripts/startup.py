#!/bin/bash

from apiconsumer.tasks import feed_sources_sync, feed_headlines_sync
from dotenv import load_dotenv

load_dotenv('/code/.env')

feed_sources_sync()
feed_headlines_sync()