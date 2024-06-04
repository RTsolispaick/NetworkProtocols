import argparse
from typing import Iterator, Optional

from app import api


def _print_info(
    user_id: str, command_name: str, infos: Optional[Iterator[object]]
) -> None:
    print(f"\nCommand {command_name} result for user_id={user_id}:\n")

    if infos is None:
        print("Incorrect user_id.")
    else:
        for info in infos:
            fields = [attr for attr in dir(info) if not callable(getattr(info, attr)) and not attr.startswith("__")]

            for field in fields:
                value = getattr(info, field)
                print(f" {field}: {value}")
            print("-------------------------------")
        print()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VK API client to fetch user data.")
    parser.add_argument("user_id", help="VK user ID.")
    parser.add_argument(
        "-f",
        "--friends",
        action="store_true",
        help="Print friends of the user.",
    )
    parser.add_argument(
        "-a",
        "--albums",
        action="store_true",
        help="Print albums of the user.",
    )
    parser.add_argument(
        "-u",
        "--userinfo",
        action="store_true",
        help="Print user info.",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        help="Specify the number of records to fetch. Default is all records.",
    )

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    user_id = args.user_id
    count = args.count if args.count and args.count > 0 else None

    if args.userinfo:
        _print_info(user_id, "userinfo", api.get_user_info(user_id))

    if args.friends:
        _print_info(user_id, "friends", api.get_user_friends(user_id, count))

    if args.albums:
        _print_info(user_id, "albums", api.get_user_albums(user_id, count))


if __name__ == '__main__':
    main()
