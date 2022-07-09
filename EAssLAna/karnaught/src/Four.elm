module Four exposing (..)


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
