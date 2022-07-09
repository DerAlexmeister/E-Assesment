module MapColoring exposing (..)

import Array as A
import Browser
import EverySet as S
import Four exposing (Index(..), Karnaugh, enumFour, get2d, repeat)
import Html exposing (Html, button, div, p, table, td, text, th, tr)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)
import Json.Decode exposing (index)
import List as L


type State
    = Marking Int
    | Idle (Maybe Int)


type alias Selection =
    S.EverySet ( Index, Index )


type alias Model =
    { karnaugh : Karnaugh
    , coloring : A.Array Selection
    , state : State
    }


type Message
    = ClickKarnaugh Index Index
    | AddColor
    | RemoveColor
    | FinishColoring
    | SelectColor Int



--| ActivateColor


main : Program () Model Message
main =
    Browser.sandbox
        { init = init
        , view = view
        , update = update
        }


init : Model
init =
    { karnaugh = repeat (repeat False)
    , coloring = A.empty
    , state = Idle Nothing
    }


update : Message -> Model -> Model
update msg model =
    case ( msg, model.state ) of
        ( AddColor, Idle _ ) ->
            { model
                | state = Marking <| A.length model.coloring
                , coloring = A.push S.empty model.coloring
            }

        ( RemoveColor, Idle (Just index) ) ->
            let
                new_coloring =
                    model.coloring
                        |> A.indexedMap Tuple.pair
                        |> A.filter (\( i, _ ) -> i == index)
                        |> A.map Tuple.second
            in
            { model | coloring = new_coloring }

        ( SelectColor index, Idle _ ) ->
            { model | state = Idle (Just index) }

        ( ClickKarnaugh x y, Marking index ) ->
            case A.get index model.coloring of
                Just working_set ->
                    let
                        new_set =
                            S.insert ( x, y ) working_set
                    in
                    { model | coloring = A.set index new_set model.coloring }

                Nothing ->
                    model

        ( FinishColoring, Marking index ) ->
            { model | state = Idle (Just index) }

        ( FinishColoring, Idle index ) ->
            { model | state = Idle index }

        _ ->
            model


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


viewKarnaugh : Karnaugh -> Html Message
viewKarnaugh karnaugh =
    table [] (L.map (viewRow karnaugh) enumFour)


indexToString : Index -> String
indexToString index =
    case index of
        Zero ->
            "00"

        One ->
            "01"

        Two ->
            "11"

        Three ->
            "10"


entryToString : Index -> Index -> String
entryToString x y =
    indexToString x ++ indexToString y


viewSelection : Int -> Selection -> Html Message
viewSelection index selection =
    S.toList selection
        |> L.map (\( x, y ) -> entryToString x y)
        |> String.join ", "
        |> text
        |> L.singleton
        |> button [ onClick <| SelectColor index ]


viewColoring : Maybe Int -> A.Array Selection -> Html Message
viewColoring index coloring =
    coloring
        |> A.indexedMap viewSelection
        |> A.indexedMap
            (\i t ->
                p
                    (if Just i == index then
                        [ style "background-color" "red" ]

                     else
                        []
                    )
                    [ t ]
            )
        |> A.toList
        |> div []


view : Model -> Html Message
view model =
    let
        index =
            case model.state of
                Marking i ->
                    Just i

                Idle i ->
                    i
    in
    div []
        [ viewKarnaugh model.karnaugh
        , viewColoring index model.coloring
        , button [ onClick AddColor ] [ text "Add Color" ]
        , button [ onClick RemoveColor ] [ text "Remove Color" ]
        , button [ onClick FinishColoring ] [ text "Finish Selection" ]
        ]
