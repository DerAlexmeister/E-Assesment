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


fromList : List a -> Maybe (Four a)
fromList l =
    case l of
        [ zero, one, two, three ] ->
            Just
                { zero = zero
                , one = one
                , two = two
                , three = three
                }

        _ ->
            Nothing


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


fromInt : Int -> Maybe Index
fromInt index =
    case index of
        0 ->
            Just Zero

        1 ->
            Just One

        2 ->
            Just Two

        3 ->
            Just Three

        _ ->
            Nothing


encode : (a -> E.Value) -> Four a -> E.Value
encode e four =
    toList four
        |> E.list e


decoder : D.Decoder a -> D.Decoder (Four a)
decoder a =
    D.list a
        |> D.map fromList
        |> D.andThen
            (\parsed ->
                case parsed of
                    Just four ->
                        D.succeed four

                    Nothing ->
                        D.fail "There must be exactly four elements in this List!"
            )


charToBool : Char -> D.Decoder Bool
charToBool c =
    case c of
        '0' ->
            D.succeed False

        '1' ->
            D.succeed True

        _ ->
            D.fail "Char must be 0 or 1!"


stackDecoder : Four Char -> D.Decoder (Four Bool)
stackDecoder four =
    D.map4 Four
        (charToBool four.zero)
        (charToBool four.one)
        (charToBool four.two)
        (charToBool four.three)


listDecoder : List a -> D.Decoder (Four a)
listDecoder list =
    case fromList list of
        Just four ->
            D.succeed four

        Nothing ->
            D.fail "There must be exactly four elements in this List!"


karnaughRow : D.Decoder (Four Bool)
karnaughRow =
    D.string
        |> D.map String.toList
        |> D.andThen listDecoder
        |> D.andThen stackDecoder


karnaugh : D.Decoder Karnaugh
karnaugh =
    decoder karnaughRow


encodeKarnaughRow : Four Bool -> E.Value
encodeKarnaughRow four =
    four
        |> map
            (\b ->
                if b then
                    '1'

                else
                    '0'
            )
        |> toList
        |> String.fromList
        |> E.string


encodeKarnaugh : Karnaugh -> E.Value
encodeKarnaugh =
    encode encodeKarnaughRow


decodeIndex : Int -> D.Decoder Index
decodeIndex int =
    fromInt int
        |> Maybe.map D.succeed
        |> Maybe.withDefault (D.fail "Index must be between 0 and 3!")
