from sntp_server.sntp_verver import SNTPServer


def main():
    try:
        SNTPServer().run()
    except Exception:
        pass


if __name__ == '__main__':
    main()