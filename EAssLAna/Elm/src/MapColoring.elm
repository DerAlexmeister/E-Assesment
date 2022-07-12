module MapColoring exposing (..)

import AllDict as D
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
    , colors : A.Array Selection
    , colorings : D.Dict ( Index, Index ) (S.EverySet Int)
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
    , colors = A.empty
    , colorings = D.empty
    , state = Idle Nothing
    , variables = Four "x1" "x2" "x3" "x4"
    }


removeColoring : Model -> Int -> Model
removeColoring model index =
    let
        new_colors =
            model.colors
                |> A.indexedMap Tuple.pair
                |> A.filter (\( i, _ ) -> i /= index)
                |> A.map Tuple.second

        new_colorings =
            model.colorings
                |> D.map (S.remove index)
    in
    { model | colors = new_colors, colorings = new_colorings }


update : Message -> Model -> Model
update msg model =
    case ( msg, model.state ) of
        ( AddColor, _ ) ->
            { model
                | state = Marking <| A.length model.colors
                , colors = A.push S.empty model.colors
            }

        ( RemoveColor, Marking index ) ->
            removeColoring model index

        ( RemoveColor, Idle (Just index) ) ->
            removeColoring model index

        ( SelectColor index, _ ) ->
            { model | state = Marking index }

        ( ClickKarnaugh x y, Marking index ) ->
            case A.get index model.colors of
                Just working_set ->
                    let
                        new_set =
                            S.insert ( x, y ) working_set

                        new_coloring =
                            S.insert index <|
                                case D.get ( x, y ) model.colorings of
                                    Just colors ->
                                        colors

                                    Nothing ->
                                        S.empty
                    in
                    { model
                        | colors = A.set index new_set model.colors
                        , colorings = D.insert ( x, y ) new_coloring model.colorings
                    }

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
    th []
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
        |> Four.map (\t -> th [] [ t ])
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
        [ chooseColoring model x y
            |> (\t ->
                    applyColoring t
                        (button
                            [ onClick (ClickKarnaugh x y) ]
                            [ text (fromBool (get2d x y model.karnaugh)) ]
                        )
               )
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
    div [] <|
        L.foldr tryAppend [] <|
            [ Just <| viewKarnaugh model.variables model
            , Just <| viewColoring index model.colors
            , addColorButton model
            , removeColorButton model
            , finishColoringButton model
            ]


try : Bool -> a -> Maybe a
try pred a =
    if pred then
        Just a

    else
        Nothing


tryAppend : Maybe a -> List a -> List a
tryAppend ma l =
    case ma of
        Just a ->
            a :: l

        Nothing ->
            l


addColorButtonStyle : List (Html.Attribute Message)
addColorButtonStyle =
    [ onClick AddColor, class "add-color", class "coloring-button" ]


addColorButton : Model -> Maybe (Html Message)
addColorButton model =
    try (A.length model.colors < L.length colorNames) <|
        button
            addColorButtonStyle
            [ text "Add Color" ]


removeColorButtonStyle : List (Html.Attribute Message)
removeColorButtonStyle =
    [ onClick RemoveColor
    , class "remove-color"
    , class "coloring-button"
    ]


removeColorButton : Model -> Maybe (Html Message)
removeColorButton model =
    case model.state of
        Marking _ ->
            try (A.length model.colors >= 1) <|
                button
                    removeColorButtonStyle
                    [ text "Remove Color" ]

        _ ->
            Nothing


finishColoringButtonStyle : List (Html.Attribute Message)
finishColoringButtonStyle =
    [ onClick FinishColoring
    , class "finish-coloring-color"
    , class "coloring-button"
    ]


finishColoringButton : Model -> Maybe (Html Message)
finishColoringButton model =
    case model.state of
        Marking _ ->
            Just <|
                button
                    finishColoringButtonStyle
                    [ text "Finish Selection" ]

        _ ->
            Nothing


chooseColoring : Model -> Index -> Index -> List (Maybe String)
chooseColoring model x y =
    let
        mapping =
            D.get ( x, y ) model.colorings
                |> Maybe.map
                    (\colors ->
                        \index color ->
                            if S.member index colors then
                                Just color

                            else
                                Nothing
                    )
                |> Maybe.withDefault (\_ _ -> Nothing)
    in
    colorNames
        |> L.indexedMap mapping


applyColoring : List (Maybe String) -> Html msg -> Html msg
applyColoring colors inner =
    L.foldl coloringStyle inner colors


activeColoringFrameStyle : List (Html.Attribute msg)
activeColoringFrameStyle =
    [ style "border-style" "dashed"
    ]


deactiveColoringFrameStyle : List (Html.Attribute msg)
deactiveColoringFrameStyle =
    [ style "border-color" "white"
    , style "border-style" "solid"
    ]


coloringFrameStyle : List (Html.Attribute msg)
coloringFrameStyle =
    [ style "padding" "2px"
    , style "margin" "2px "
    ]


coloringStyle : Maybe String -> Html msg -> Html msg
coloringStyle color inner =
    color
        |> Maybe.map (style "border-color")
        |> Maybe.map L.singleton
        |> Maybe.map (L.append activeColoringFrameStyle)
        |> Maybe.withDefault deactiveColoringFrameStyle
        |> L.append coloringFrameStyle
        |> (\attr -> div attr [ inner ])


colorNames : List String
colorNames =
    [ "red", "green", "blue", "purple", "black" ]
