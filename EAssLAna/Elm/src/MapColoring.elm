module MapColoring exposing (..)

import Array as A
import Browser
import EverySet as S
import Four exposing (Four, Index(..), Karnaugh, enumFour, get2d, repeat)
import Html exposing (Html, button, div, p, table, td, text, th, tr)
import Html.Attributes exposing (class, style)
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
    , variables : Four String
    }


type Message
    = ClickKarnaugh Index Index
    | AddColor
    | RemoveColor
    | FinishColoring
    | SelectColor Int


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
    , variables = Four "x1" "x2" "x3" "x4"
    }


removeColoring : Model -> Int -> Model
removeColoring model index =
    let
        new_coloring =
            model.coloring
                |> A.indexedMap Tuple.pair
                |> A.filter (\( i, _ ) -> i /= index)
                |> A.map Tuple.second
    in
    { model | coloring = new_coloring }


update : Message -> Model -> Model
update msg model =
    case ( msg, model.state ) of
        ( AddColor, _ ) ->
            { model
                | state = Marking <| A.length model.coloring
                , coloring = A.push S.empty model.coloring
            }

        ( RemoveColor, Marking index ) ->
            removeColoring model index

        ( RemoveColor, Idle (Just index) ) ->
            removeColoring model index

        ( SelectColor index, _ ) ->
            { model | state = Marking index }

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


rowValues : Four String
rowValues =
    Four "00" "01" "11" "10"


columnValues : Four String
columnValues =
    Four "10" "11" "01" "00"


entryToString : Index -> Index -> String
entryToString x y =
    Four.get x rowValues ++ Four.get y columnValues


tableCaption : Four String -> Html msg
tableCaption four =
    th [ captionClass ]
        [ text <|
            four.two
                ++ four.three
                ++ "\\"
                ++ four.zero
                ++ four.one
        ]


rowCaption : Four String -> Html msg
rowCaption variables =
    rowValues
        |> Four.map text
        |> Four.map (\t -> th [ captionClass ] [ t ])
        |> Four.toList
        |> (\l -> tableCaption variables :: l)
        |> tr []


columnCaption : Index -> Html msg
columnCaption index =
    columnValues
        |> Four.get index
        |> text


viewDatum : Model -> Index -> Index -> Html Message
viewDatum model x y =
    td []
        [ button
            [ datumClass
            , onClick (ClickKarnaugh x y)
            ]
            [ text (fromBool (get2d x y model.karnaugh)) ]
        ]


viewRow : Model -> Index -> Html Message
viewRow model x =
    tr [] (columnCaption x :: L.map (viewDatum model x) enumFour)


viewKarnaugh : Four String -> Model -> Html Message
viewKarnaugh variables model =
    enumFour
        |> L.map (viewRow model)
        |> (\l -> rowCaption variables :: l)
        |> table []


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
        [ viewKarnaugh model.variables model
        , viewColoring index model.coloring
        , button [ onClick AddColor ] [ text "Add Color" ]
        , button [ onClick RemoveColor ] [ text "Remove Color" ]
        , button [ onClick FinishColoring ] [ text "Finish Selection" ]
        ]


captionClass =
    class "caption"


activeClass =
    class "active"


coloringClass index =
    class <| "coloring" ++ String.fromInt index


datumClass =
    class "datum"
