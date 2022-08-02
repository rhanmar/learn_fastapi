from typing import List, Optional, Union
from fastapi import FastAPI, HTTPException, status, Query, Path
from pydantic.fields import Required

from models import Style, Type, Artist


app = FastAPI()


styles: List[Style] = [
    Style(
        id=1,
        name="Muay Thai",
        type=Type.kick
    ),
    Style(
        id=2,
        name="BJJ",
        type=Type.wrestling
    ),
    Style(
        id=3,
        name="MMA",
        type=Type.mixed
    ),
    Style(
        id=4,
        name="Boxing",
        type=Type.kick
    ),
    Style(
        id=5,
        name="Wrestling",
        type=Type.wrestling
    ),
]


artists: List[Artist] = [
    Artist(
        id=1,
        name="Conor McGregor",
        styles=[styles[2], styles[3]],
    ),
    Artist(
        id=2,
        name="Khabib",
        styles=[styles[2], styles[4]],
    ),
]


@app.get('/')
def root() -> dict:
    return {"Welcome": "Martial"}


@app.get("/api/styles")
def get_styles(number: int = Query(default=None, gt=0, lt=len(styles))) -> Union[List[Style], Style]:
    if number:
        try:
            return styles[number]
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Style by number {number} does not exist."
            )
    return styles


@app.get("/api/test_queries")
def test_queries(
        q: List[str] = Query(
            default=Required,
            title="Test query!!",
            description="Test description!!",
            alias="q-q",
            deprecated=True,
            # include_in_schema=False
        )
):  # default=...
    return q


@app.get("/api/{type_name}")
def get_type(type_name: Type):
    return type_name


@app.get("/api/styles/{style_id}")
def get_style_by_id(q: str = None, style_id: int = Path(title="Style_id", gt=1, description="n>1", default=...)) -> Style:
    for style in styles:
        if style.id == style_id:
            return style
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Style with id {style_id} does not exist."
    )


@app.post("/api/styles", status_code=status.HTTP_201_CREATED)
def create_style(style: Style) -> dict:
    styles.append(style)
    return {
        "id": style.id,
        "name": style.name,
        "type": style.type,
    }


@app.put("/api/styles/{style_id}")
def put_style(style_id: int, style_info: Style):
    for item in styles:
        if item.id == style_id:
            item.name = style_info.name
            item.type = style_info.type
            return {"response": f"style with id {style_id} changed"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Style with id {style_id} does not exist."
    )


@app.delete("/api/styles/{style_id}", status_code=status.HTTP_201_CREATED)
def delete_style(style_id: int):
    for item in styles:
        if item.id == style_id:
            styles.remove(item)
            return {"response": f"item with id {style_id} was removed"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Style with id {style_id} does not exist."
    )


@app.get("/api/artists")
def get_artists(name: str = None) -> Union[List[Artist], Artist]:
    if name is not None:
        return list(filter(lambda x: x.name == name, artists))[0]
    return artists


@app.get("/api/artists/{artist_id}")
def get_artist_by_id(artist_id: int) -> Artist:
    try:
        return list(filter(lambda x: x.id == artist_id, artists))[0]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artist with id {artist_id} does not exist."
        )
