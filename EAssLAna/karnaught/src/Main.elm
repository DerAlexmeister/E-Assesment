module Main exposing (..)

import Browser
import Four exposing (Index, Karnaugh, enumFour, get2d, repeat, set2d)
import Html exposing (Html, button, div, table, td, text, tr)
import Html.Events exposing (onClick)
import List as L


type alias Model =
    { karnaugh : Karnaugh
    }


type Message
    = ClickedMap Index Index


main =
    Browser.sandbox
        { init = { karnaugh = repeat (repeat False) }
        , update = update
        , view = view
        }


update : Message -> Model -> Model
update msg model =
    case msg of
        ClickedMap x y ->
            let
                v =
                    not (get2d x y model.karnaugh)
            in
            { model | karnaugh = set2d x y v model.karnaugh }


fromBool : Bool -> String
fromBool b =
    if b then
        "1"

    else
        "0"


viewDatum : Karnaugh -> Index -> Index -> Html Message
viewDatum karnaugh x y =
    td []
        [ button
            [ onClick (ClickedMap x y) ]
            [ text (fromBool (get2d x y karnaugh)) ]
        ]


viewRow : Karnaugh -> Index -> Html Message
viewRow karnaugh x =
    tr [] (L.map (viewDatum karnaugh x) enumFour)


view : Model -> Html Message
view model =
    table [] (L.map (viewRow model.karnaugh) enumFour)
