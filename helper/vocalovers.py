# Notes:
import sys
import json
from pathlib import Path
from typing import Any

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Medium,
    Circle,
    Event,
    EventGroup,
    Source,
    ReliabilityTypes,
    OriginTypes,
    Location,
)

RT, OT = ReliabilityTypes, OriginTypes

PATH_HELPER = Path(__file__).parent
PATH_EVENT_GROUP = PATH_HELPER.parent
PATH_MEDIA = PATH_EVENT_GROUP / "media"


def retrieve_circles(event_name: str) -> list[Circle]:
    """Retrieve circles of given event. In the circle file has not been created, execute the creation script first."""
    circles_json_path = PATH_HELPER / event_name / "circles.json"
    if not circles_json_path.exists():
        print(
            f"Circle file for {event_name} not found, running the creation script ..."
        )
        creation_script_path = PATH_HELPER / event_name / "main.py"
        if not creation_script_path.exists():
            raise FileNotFoundError(
                f"Creation script for {event_name} not found at {creation_script_path}"
            )
        # Import main() from the creation script and execute
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            f"{event_name}.main", creation_script_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                module.main()

        if not circles_json_path.exists():
            raise FileNotFoundError(
                f"Creation script {creation_script_path} failed to create {circles_json_path}"
            )

    with circles_json_path.open("r", encoding="utf-8") as f:
        circles_raw = json.load(f)
    return [Circle.load_from_json(c) for c in circles_raw]


if __name__ == "__main__":
    events: list[Event] = []
    active_events: list[int | str] = [1]

    i = 1  # ==== vocalovers ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        index_url = (
            "https://web.archive.org/web/20120113155155/http://vocalovers.jimdo.com/"
        )

        media_ = []
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d11280.11385310613!2d130.70241807455395!3d32.80291548325864!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3540f412baa3593f%3A0x39fe3c93d447391e!2sKumamoto%20City%20International%20Center!5e0!3m2!1sen!2sfr!4v1781473683057!5m2!1sen!2sfr",
                description="熊本市国際交流会館",
                sources=[
                    Source(
                        'https://x.com/vocalovers_0108/status/137083060968624129',
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    ),
                ],
            ),
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d11280.11385310613!2d130.70241807455395!3d32.80291548325864!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3540f412baa3593f%3A0x39fe3c93d447391e!2sKumamoto%20City%20International%20Center!5e0!3m2!1sen!2sfr!4v1781473683057!5m2!1sen!2sfr",
                description="(After event) 地下二階・多目的ルーム ",
                sources=[
                    Source(
                        "https://web.archive.org/web/20120127201933/http://vocalovers.jimdo.com/%E3%82%A2%E3%83%95%E3%82%BF%E3%83%BC%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88%E8%A9%B3%E7%B4%B0/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                "VOCALOID LOVERS",
                "ボーカロイドラバーズ",
                "ボカラー",
                "vocalovers",
            ],
            dates="2012.01.08",
            circles=[],
            media=media_,
            sources=[
                Source(f"Date: {index_url}", (RT.Reliable, OT.Official)),
                # Source("Participating circles: ", (RT.Reliable, OT.Official)),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.06.14",
        )

        # Retrieve circles
        # event.circles = retrieve_circles(event_name)
        events.append(event)

    # ==== event group ====
    media = [
        Medium("20130704152505_header.jpg",
               [Source("https://web.archive.org/web/20130704152505/http://vocalovers.jimdo.com:80/", (RT.Reliable, OT.Official))]),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
    ]
    links = [
        "https://web.archive.org/web/20120113155155/http://vocalovers.jimdo.com/",
    ]

    event_group = EventGroup(
        aliases=["VOCALOID LOVERS", "ボーカロイドラバーズ", "ボカラー", "vocalovers"],
        events=events,
        media=media,
        links=links,
        sources=[
            Source(
                'Alias "ボカラー": https://web.archive.org/web/20120127215205/http://vocalovers.jimdo.com/%E7%89%B9%E5%85%B8/',
                (ReliabilityTypes.Reliable, OriginTypes.Official),
            ),
            Source(
                'Alias "vocalovers": main site url',
                (ReliabilityTypes.Reliable, OriginTypes.Official),
            ),
            # Source(
            #     "",
            #     (ReliabilityTypes.Reliable, OriginTypes.Official),
            # ),
        ],
        comments="Two circles are known to have participated in the event: '蒼音-souon-'(C-02) and '熊本WOTAKUrank': https://web.archive.org/web/20120127223632/http://vocalovers.jimdo.com/%E9%80%9F%E5%A0%B1/",
        description=None,
        # last_edited="",
    )

    print(f"Saving {Path(__file__).stem} database...")
    event_group.save(PATH_EVENT_GROUP, indent=None)
    print("Done")
