#!/usr/bin/env python3
"""Servidor local do Escuta.

Serve esta pasta e, se o cloudflared estiver instalado, cria um link HTTPS
temporário (https://....trycloudflare.com) para abrir no celular. O iPhone só
libera o microfone em HTTPS, então o endereço da rede local (http://192.168...)
abre a página mas não deixa escutar.

Uso:  python3 servir.py [--porta 8000] [--sem-tunel]
"""
import argparse
import functools
import http.server
import os
import re
import shutil
import socket
import subprocess
import sys
import threading

PASTA = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.webmanifest': 'application/manifest+json',
        '.js': 'text/javascript',
        '.svg': 'image/svg+xml',
    }

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


def ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()


def mostrar_qr(url):
    try:
        import qrcode  # pip install qrcode (opcional)
    except ImportError:
        return
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.print_ascii(invert=True)


def tunel(porta):
    cmd = ['cloudflared', 'tunnel', '--no-autoupdate', '--url', f'http://localhost:{porta}']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for linha in proc.stdout:
        m = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', linha)
        if m:
            url = m.group(0)
            print('\n  Abra no iPhone (HTTPS, microfone liberado):\n')
            print(f'    {url}\n')
            mostrar_qr(url)
            print('  O link muda a cada execução e para de funcionar quando você fechar este programa.\n')
            break
    # Continua lendo para o cloudflared não travar com o buffer cheio.
    threading.Thread(target=lambda: [None for _ in proc.stdout], daemon=True).start()
    return proc


def main():
    ap = argparse.ArgumentParser(description='Servidor local do Escuta')
    ap.add_argument('--porta', type=int, default=8000)
    ap.add_argument('--sem-tunel', action='store_true', help='não criar link HTTPS com cloudflared')
    args = ap.parse_args()

    handler = functools.partial(Handler, directory=PASTA)
    srv = http.server.ThreadingHTTPServer(('0.0.0.0', args.porta), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    print(f'\n  Escuta rodando em http://localhost:{args.porta}')
    print(f'  Rede local: http://{ip_local()}:{args.porta}  (no iPhone o microfone exige HTTPS)')

    proc = None
    if not args.sem_tunel:
        if shutil.which('cloudflared'):
            print('  Criando link HTTPS com cloudflared…')
            proc = tunel(args.porta)
        else:
            print('\n  Para testar no iPhone, instale o cloudflared e rode de novo:')
            print('    macOS:   brew install cloudflared')
            print('    Windows: winget install --id Cloudflare.cloudflared')
            print('    Linux:   https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/')
    print('\n  Ctrl+C para encerrar.\n')
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        srv.shutdown()
        if proc:
            proc.terminate()
        print('\n  Encerrado.')
        sys.exit(0)


if __name__ == '__main__':
    main()
