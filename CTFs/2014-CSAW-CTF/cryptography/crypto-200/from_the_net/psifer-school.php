<?php
    class Vigenere {
        public static $mVigTable;
        public static $mKey;
        public static $mMod;
        final public function __construct($rKey = false, $rVigTable = false)
        {
            self::$mVigTable = $rVigTable ? $rVigTable : 'abcdefghijklmnopqrstuvwxyz';
            self::$mMod = strlen(self::$mVigTable);
            self::$mKey = $rKey ? $rKey : self::generateKey();
        }
        final public function getKey()
        {
            return self::$mKey;
        }
        private function getVignereIndex($iPos)
        {
            return strpos(self::$mVigTable, $iPos); // todo: catch chars not in table
        }
        private function getVignereChar($rVignereIndex)
        {
            (int)$iVignereIndex = $rVignereIndex;
            $iVignereIndex=$iVignereIndex>=0 ? $iVignereIndex : strlen(self::$mVigTable)+$iVignereIndex;
            return self::$mVigTable{$iVignereIndex};
        }
        final public function generateKey()
        {
            self::$mKey = '';
            for ($i = 0; $i < self::$mMod; $i++) {
                self::$mKey .= self::$mVigTable{rand(0, self::$mMod)};
            }
            return self::$mKey;
        }
        final public function encrypt($rText, $rKey)
        {
            $sEncryptValue = '';
            $sKey  = (String)$rKey;
            $sText = (String)$rText;

            for($i = 0; $i < strlen($sText); $i++)
            {
                (int)$iText  = self::getVignereIndex($sText[$i]);
                (int)$iKey   = self::getVignereIndex(self::charAt($sKey, $i));

                $iEncryptIndex = ($iText+$iKey)%(self::$mMod);
                $iEncryptIndex = self::EnsureKeyValid($iEncryptIndex);
                $sEncryptValue .= self::getVignereChar($iEncryptIndex);
            }
            return $sEncryptValue;
        }
        final public function encrypt2($rText, $rKey, $rMod)
        {
            (String)$sEncryptValue  = '';
            $sKey  = (String)$rKey;
            $sText = (String)$rText;
            $iMod  = (int)$rMod;

            for($i = 0; $i < strlen($sText); $i++)
            {
                (int)$iText  = self::getVignereIndex($sText[$i]);
                (int)$iKey   = self::getVignereIndex(self::charAt($sKey, $i));

                $iEncryptIndex = ($iText+$iKey)%($iMod);
                $iEncryptIndex = self::EnsureKeyValid($iEncryptIndex);
                $sEncryptValue .= self::getVignereChar($iEncryptIndex);
            }
            return $sEncryptValue;
        }
        final public function decrypt($rText, $rKey)
        {
            (String)$sDecryptValue = '';
            $sKey  = (String)$rKey;
            $sText = (String)$rText;

            for($i = 0; $i < strlen($sText); $i++)
            {
                (int)$iText  = self::getVignereIndex($sText[$i]);
                (int)$iKey   = self::getVignereIndex(self::charAt($sKey, $i));

                $iDecryptIndex = ($iText-$iKey)%(self::$mMod);
                $iDecryptIndex  = self::EnsureKeyValid($iDecryptIndex);

                $sDecryptValue .= self::getVignereChar($iDecryptIndex);
            }
            return $sDecryptValue;
        }
        final public function decrypt2($rText, $rKey, $rMod)
        {
            (String)$sDecryptValue  = '';
            $sKey  = (String)$rKey;
            $sText = (String)$rText;
            $iMod  = (int)$rMod;

            for($i = 0; $i < strlen($sText); $i++)
            {
                (int)$iText  = self::getVignereIndex($sText[$i]);
                (int)$iKey   = self::getVignereIndex(self::charAt($sKey, $i));


                $iDecryptIndex  = ($iText-$iKey)%($iMod);
                $iDecryptIndex  = self::EnsureKeyValid($iDecryptIndex);

                $sDecryptValue .= self::getVignereChar($iDecryptIndex);
            }
            return $sDecryptValue;
        }
        private function charAt($rStr, $rPos)
        {
            $iPos = (int)$rPos%strlen((String)$rStr);

            return $rStr{$iPos};
        }

        private function EnsureKeyValid($rIndex)
        {
            $iIndex = (int)$rIndex;
            return ($iIndex >= 0) ? $iIndex : (strlen(self::$mVigTable)+$iIndex);
        }

    }

    function decrypt_final($key,$text){
        $text = str_replace(" ","", strtolower($text));
        $key  = $key;
        $plain= new Vigenere($key);
        $plain= $plain->decrypt($text,$key);
        return strtoupper($plain);
    }

    function str_rot($s, $n = 13) {
        $n = (int)$n % 26;
        if (!$n) return $s;
        for ($i = 0, $l = strlen($s); $i < $l; $i++) {
            $c = ord($s[$i]);
            if ($c >= 97 && $c <= 122) {
                $s[$i] = chr(($c - 71 + $n) % 26 + 97);
            } else if ($c >= 65 && $c <= 90) {
                $s[$i] = chr(($c - 39 + $n) % 26 + 65);
            }
        }
        return $s;
    }

    function inStr ($needle, $haystack) { // instr("test","testtest");
      $needlechars = strlen($needle);
      $i = 0;
      for($i=0; $i < strlen($haystack); $i++)
      {
        if(substr($haystack, $i, $needlechars) == $needle)
        {
          return TRUE;
        }
      }
      return FALSE;
    }

    $usenet = fsockopen("54.209.5.48", "12345", $errno, $errstr, 3);
    first:
    while (!feof($usenet)) {
        $kp = fgets($usenet, 128);
        if(inStr("psifer text:", $kp)){
            $kp = explode("psifer text: ", $kp);
            $kp = $kp[1];
            $kp = explode("\n", $kp);
            $kp = $kp[0];
            for($i=0;$i<25;$i++){
                $temp = str_rot($kp, $i) . "\n";
                if(instr("the answer to this stage is" , $temp)){
                    $temp = explode("the answer to this stage is " , $temp);
                    $temp = $temp[1];
                    goto second;
                }
            }
        }
    }
    second:
    fputs($usenet, $temp);
    while (!feof($usenet)) {
        $kp = fgets($usenet, 260);
        if(inStr("psifer text:", $kp)){
            $kp = explode("psifer text: ", $kp);
            $kp = $kp[1];
            $possible_flag = array("easiest answer", "more answers here", "winning for the win", "tired of making up bogus answers", "not not wrong");
            $possible_guess= rand(0,2);
            fputs($usenet, $possible_flag[$possible_guess] . "\n");
            goto third;
        }
    }
    third:
    while (!feof($usenet)) {
        if(!$usenet) die("error.");
        $kp = fgets($usenet, 8192);
        if(inStr("psifer text:", $kp)){
            $kp = explode("psifer text: ", $kp);
            $kp = $kp[1];
            /*
            echo @decrypt_final("force",$kp) . "\n----\n";
            echo @decrypt_final("tobrute",$kp) . "\n----\n";
            echo @decrypt_final("dictionary",$kp) . "\n----\n";
            echo @decrypt_final("diary",$kp) . "\n----\n";
            */
            if(inStr("HISTIMEWEWILLGIVEYOU",@decrypt_final("force",$kp))){
                $temp = @decrypt_final("force",$kp);
                $temp = explode("DLERIGHTHERE",$temp);
                $temp = $temp[1];
                $temp = explode("OKNOW",$temp);
                $temp = $temp[0];
                fputs($usenet, $temp);
            }elseif(inStr("HISTIMEWEWILLGIVEYOU",@decrypt_final("tobrute",$kp))){
                $temp = @decrypt_final("tobrute",$kp);
                $temp = explode("DLERIGHTHERE",$temp);
                $temp = $temp[1];
                $temp = explode("OKNOW",$temp);
                $temp = $temp[0];
                fputs($usenet, $temp);
            }elseif(inStr("HISTIMEWEWILLGIVEYOU",@decrypt_final("dictionary",$kp))){
                $temp = @decrypt_final("tobrute",$kp);
                $temp = explode("DLERIGHTHERE",$temp);
                $temp = $temp[1];
                $temp = explode("OKNOW",$temp);
                $temp = $temp[0];
                fputs($usenet, $temp);
            }elseif(inStr("HISTIMEWEWILLGIVEYOU",@decrypt_final("diary",$kp))){
                $temp = @decrypt_final("diary",$kp);
                $temp = explode("DLERIGHTHERE",$temp);
                $temp = $temp[1];
                $temp = explode("OKNOW",$temp);
                $temp = $temp[0];
                fputs($usenet, $temp);
            }
            fputs($usenet,"\n");
            $kp = fgets($usenet, 8192);
            echo $kp;
        }
    }


?>