from nose import tools

from h10n.server.locale import Locale


def locale_test():
    en_us = Locale(
        'en-US',
        {
            'on_start_up':{
                'strategy': 'on_start_up',
                'source': [
                    {
                        'id': 'message',
                        'msg': 'Message 1',
                    }
                ]
            },
            'on_demand': {
                'strategy': 'on_demand',
                'source': {
                    'message': {
                        'msg': 'Message 2',
                    }
                }
            }
        }
    )
    tools.eq_(en_us['on_start_up.message'].format(), 'Message 1')
    tools.eq_(en_us['on_demand.message'].format(), 'Message 2')
