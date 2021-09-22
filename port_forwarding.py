# -*- coding: utf-8 -*-
import PySimpleGUI as sg
from peer_connection import Server


def main():
    sg.theme('TanBlue')
    layout = [
          [sg.Text('本地地址'), sg.InputText('', size=(16, 1), key='local_addr'),
           sg.Text('本地端口'), sg.InputText('大于1024', key='local_port', size=(10, 1)),
           sg.Text('远端地址'), sg.InputText('', key='remote_addr', size=(16, 1)),
           sg.Text('远端端口'), sg.InputText('', key='remote_port', size=(10, 1)),
           sg.Text(' ' * 1),
           sg.Button('连接'),
           sg.Text(' ' * 1)
           ],
        [
            sg.Text('_' * 90)
         ],
        [
            sg.MLine(default_text='', size=(20 * 5), key='multi')
        ]

    ]
    window = sg.Window('端口映射工具', layout=layout, default_element_size=(6, 1), grab_anywhere=False)
    while True:
        event, values = window.read()
        if event == '连接':
            local_addr = values['local_addr']
            local_port = values['local_port']
            remote_addr = values['remote_addr']
            remote_port = values['remote_port']
            if local_addr and local_port and remote_addr and remote_port:
                try:
                    s = Server(local_addr, int(local_port), remote_addr, int(remote_port))
                    s.setDaemon(True)
                    s.start()
                    window['multi'].update('连接成功')
                except Exception as e:
                    window['multi'].update(str(e))
                    raise e
        elif event == '关闭' or event == sg.WIN_CLOSED:
            break
    window.close()


if __name__ == '__main__':
    main()
