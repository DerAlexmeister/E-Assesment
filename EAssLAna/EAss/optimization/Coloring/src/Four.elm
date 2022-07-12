module Four exposing (..)

import Json.Decode as D
import Json.Encode as E


type alias Four a =
    { zero : a
    , one : a
    , two : a
    , three : a
    }


type Index
    = Zero
    | One
    | Two
    | Three


enumFour : List Index
enumFour =
    [ Zero, One, Two, Three ]


repeat : a -> Four a
repeat a =
    Four a a a a


type alias Karnaugh =
    Four (Four Bool)


get : Index -> Four a -> a
get index four =
    case index of
        Zero ->
            four.zero

        One ->
            four.one

        Two ->
            four.two

        Three ->
            four.three


set : Index -> a -> Four a -> Four a
set index a four =
    case index of
        Zero ->
            { four | zero = a }

        One ->
            { four | one = a }

        Two ->
            { four | two = a }

        Three ->
            { four | three = a }


get2d : Index -> Index -> Four (Four a) -> a
get2d x y array =
    get x array
        |> get y


set2d : Index -> Index -> a -> Four (Four a) -> Four (Four a)
set2d x y a array =
    get x array
        |> set y a
        |> (\row -> set x row array)


map : (a -> b) -> Four a -> Four b
map f four =
    { zero = f four.zero
    , one = f four.one
    , two = f four.two
    , three = f four.three
    }


index_map : (Index -> a -> b) -> Four a -> Four b
index_map f four =
    { zero = f Zero four.zero
    , one = f One four.one
    , two = f Two four.two
    , three = f Three four.three
    }


toList : Four a -> List a
toList four =
    [ four.zero, four.one, four.two, four.three ]


toInt : Index -> Int
toInt index =
    case index of
        Zero ->
            0

        One ->
            1

        Two ->
            2

        Three ->
            3


encode : (a -> E.Value) -> Four a -> E.Value
encode e four =
    let
        keys =
            [ "0", "1", "2", "3" ]
    in
    toList four
        |> List.map e
        |> List.map2 Tuple.pair keys
        |> E.object


decoder : D.Decoder a -> D.Decoder (Four a)
decoder a =
    D.map4 Four
        (D.field "0" a)
        (D.field "1" a)
        (D.field "2" a)
        (D.field "3" a)
