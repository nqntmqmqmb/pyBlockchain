<?php
$transaction = $_POST['transaction'];
$POW = $_POST['POW'];
$i = $_POST['i'];


$arr = json_decode($transaction, true);
$from = $arr['from'];
$to = $arr['to'];
$amount = $arr['amount'];
$string = $arr['proof-of-work-word1'] . "," . $arr['proof-of-work-word2'] . '!' . $i;
$internal_pow = hash('sha256',$string);

if( strpos(file_get_contents("./mine"),$transaction) !== false) {
    
        
        if (substr($internal_pow, 0,4) === $arr['proof-of-work-startby']) {
            
            $lines  = file('mine');

            $result = '';
            foreach($lines as $line) {
                if(stripos($line, $transaction) === false) {
                    $result .= $line;
                }
            }
            file_put_contents('mine', $result);
            $block = '{"transaction":[{"from":"' . $from . '","to":"' . $to . '","amount":' . $amount . '}],"POW":"' . $internal_pow . '"}';
            echo "OK";
            $handle = fopen('NV_block', 'a');
            fwrite($handle, $block . "\n");
            fclose($handle);
        }
    
    } else {
    echo "NO";
}
?>
