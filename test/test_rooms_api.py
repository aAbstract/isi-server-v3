import _test_util


def test_get_rooms_lock():
    api_route = 'user/rooms/get-rooms'
    _test_util.assert_api_lock_invalid_token(api_route)


def test_get_rooms():
    api_route = 'user/rooms/get-rooms'
    access_tokens = [
        _test_util.login_user('test_admin', 'TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        _test_util.login_user('test_user', 'upass123'),
    ]
    rooms = _test_util.assert_api_get_struct(api_route, access_tokens, {'room_icon', 'room_name', 'id', 'room_disp_name', 'global_sensors_list'})
    main_room = [x for x in rooms if x['room_name'] == 'living_room_0']
    assert main_room
    main_room = main_room[0]
    assert set(main_room['global_sensors_list']) == {'main_humidity_sensor_0', 'main_temperature_sensor_0'}
