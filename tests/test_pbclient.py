import pytest
import pbclient
import os
import uuid

BR3_TEST_CHANNEL="br3foodtrucks_dev"

def test_push_integration():
    token = os.environ.get('PUSHBULLET_TOKEN')
    if token is None:
    	print "must set PUSHBULLET_TOKEN env variable before running this test"
    	assert 0
    test_id = str(uuid.uuid4())
    pbclient.push_note_to_channel(BR3_TEST_CHANNEL, "integration test", test_id, token)
    channel_info = pbclient.get_channel_info(BR3_TEST_CHANNEL, token)
    print test_id
    print channel_info['recent_pushes'][0]
    assert channel_info['recent_pushes'][0]['body'] == test_id
