from nose import tools

from h10n.server.server import Server


def server_test():
    """ Localization Server Test """
    server = Server(
        locales={
            'en-US': {
                'catalogs': {
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
                },
                'helpers': {
                    'fake_helper_1': 'Locale Level',
                },
            }
        },
        helpers={
            'fake_helper_1': 'Server Level',
            'fake_helper_2': 'Server Level',
        }
    )
    # Test catalogs
    tools.eq_(server['en-US.on_start_up.message'].format(), 'Message 1')
    tools.eq_(server['en-US.on_demand.message'].format(), 'Message 2')
    # Test helper overriding
    tools.eq_(server['en-US'].get_helper('fake_helper_1'), 'Locale Level')
    tools.eq_(server['en-US'].get_helper('fake_helper_2'), 'Server Level')
