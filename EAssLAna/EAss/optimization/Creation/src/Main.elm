module Main exposing (..)

import Browser
import Four exposing (Index, Karnaugh, enumFour, get2d, repeat, set2d)
import Html exposing (Html, button, div, table, td, text, tr)
import Html.Events exposing (onClick)
import Json.Decode as D
import List as L
import MapCreation as MC


type Model
    = InternalError
    | MapCreation MC.Problem Karnaugh


type Message
    = ClickKarnaugh Index Index


type alias Flag =
    { problem : D.Value }


init : Flag -> ( Model, Cmd Message )
init flag =
    ( case D.decodeValue MC.decoder flag.problem of
        Ok problem ->
            MapCreation problem (repeat (repeat False))

        Err _ ->
            InternalError
    , Cmd.none
    )


subscriptions : Model -> Sub Message
subscriptions _ =
    Sub.none


main : Program Flag Model Message
main =
    Browser.element
        { init = init
        , subscriptions = subscriptions
        , update = update
        , view = view
        }


update : Message -> Model -> ( Model, Cmd Message )
update msg model =
    case model of
        MapCreation problem karnaugh ->
            case msg of
                ClickKarnaugh x y ->
                    let
                        v =
                            not (get2d x y karnaugh)
                    in
                    ( MapCreation problem (set2d x y v karnaugh), Cmd.none )

        _ ->
            ( model, Cmd.none )


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
            [ onClick (ClickKarnaugh x y) ]
            [ text (fromBool (get2d x y karnaugh)) ]
        ]


viewRow : Karnaugh -> Index -> Html Message
viewRow karnaugh x =
    tr [] (L.map (viewDatum karnaugh x) enumFour)


view : Model -> Html Message
view model =
    case model of
        InternalError ->
            text "An internal Error occurred."

        MapCreation problem karnaugh ->
            table [] (L.map (viewRow karnaugh) enumFour)
