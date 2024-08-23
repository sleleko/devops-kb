/**
 * correct words endings after numberic values,
 * for example recieve count 5 and array of possible endings of days ['day','days','...']
 * its method will recieve correct endings for day. Work fine for russians
 *
 * @param int $number
 * @param array $endingArray
 * @return string
 */
public function getNumEnding(int $number,array $endingArray): string
{
    $number = $number % 100;
    if ($number>=11 && $number<=19) {
        $ending=$endingArray[2];
    }
    else {
        $i = $number % 10;
        $ending = match ($i) {
            1 => $endingArray[0],
            2, 3, 4 => $endingArray[1],
            default => $endingArray[2],
        };
    }
    return $ending;
}
