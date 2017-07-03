#!/usr/bin/perl

use utf8;

use strict;
use warnings;
use LWP::UserAgent;
use HTML::TreeBuilder;
use DBI;

use Encode 'encode';
use Encode 'decode';
use Encode::Guess;

my $rarity = $ARGV[0];
my $url;
my $tablesize = 18;

if($rarity==4){ $url = 'https://www59.atwiki.jp/lovelive-sif/pages/379.html'; #UR
				$tablesize = 19;
}elsif($rarity==3){ $url = 'https://www59.atwiki.jp/lovelive-sif/pages/691.html'; #SSR
				$tablesize = 19;
}elsif($rarity==2){ $url = 'https://www59.atwiki.jp/lovelive-sif/pages/711.html'; #SR
}elsif($rarity==1){ $url = 'https://www59.atwiki.jp/lovelive-sif/pages/210.html'; #R
}elsif($rarity==0){ $url = 'https://www59.atwiki.jp/lovelive-sif/pages/101.html'; #N
}

# IE8のフリをする
my $user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)";

# LWPを使ってサイトにアクセスし、HTMLの内容を取得する
my $ua = LWP::UserAgent->new('agent' => $user_agent);
my $res = $ua->get($url);
my $content = $res->content;

# HTML::TreeBuilderで解析する
my $tree = HTML::TreeBuilder->new;
$tree->parse($content);


my $user = 'web';
my $passwd = 'password';
my $db = DBI->connect('DBI:mysql:sif_event:localhost', $user, $passwd);
$db->do("set names utf8"); 

my $type = "";
my $unit_skill = "";
my $unit_skill_detail = "";
my $center_skill = "";
my $center_skill_detail = "";
my $flag = 0;


# DOM操作してトピックの部分だけ抜き出す。
# <div id='topicsfb'><ul><li>....の部分を抽出する
my $elm  = $tree->look_down('id', 'contents');
my  @list =  $elm->find('tr');
for my $tr (@list) {

	if($rarity == 4 && $flag == 0){
		$flag = 1;
		next;
	}

	my @table = $tr->find('td');
	if((defined($table[0]) && defined($table[2])) && $#table < 20 && $#table > 10){

		print "table size : ".$#table."\n";

		my $col = 0;
		if($tablesize==19) {$col=1};

    	my $id = $table[$col]->as_text;

		my @image_tag = $table[$col+1]->find('img');
#		my $image_url = "http:".$image_tag[0]->attr('src');
		my $image_url = "";

		my @names;
		my $name, my $series;
		my $imple_info;
		my @imple_infos;
		my $name_series;

		my $get_method;


		if(defined($table[$col+2]->find('span'))){
			# 実装日時の代入
			@imple_infos = $table[$col+2]->find('span');
			$imple_info = $imple_infos[0]->as_text;
			# 実装日時と名前の分離
    		$name_series = $table[$col+2]->as_text;
			$name_series =~ s/(?:$imple_info)//g;
		}else{
			$imple_info = '';
    		$name_series = $table[$col+2]->as_text;
		}

		# 0:勧誘1:イベント2:シリアル/配布
		my $hosyu = &enu("報酬");
		my $tokuten = &enu("特典");

		if($imple_info =~ /$hosyu/){
			$get_method = 1;
		}elsif($imple_info =~ /$tokuten/){
			$get_method = 2;
		}else{
			$get_method = 0;
		}

		my $start_splitter; my $end_splitter;
		if($name_series =~/\(/){$start_splitter='\(';$end_splitter='\)';}
		elsif($name_series =~/（/){$start_splitter='（';$end_splitter='）';}

		if(defined($start_splitter)){
   			@names = split($start_splitter,$name_series);
			$name = $names[0];
			$series = $names[1];
   			$series =~ s/(?:$end_splitter)//g;
		}else{
			$name = $name_series;
			$series = "";
		}
		$name =~ s/\s//g;
		$series =~ s/\s//g;

		if($#table == $tablesize){
			$type = $table[$col+4]->as_text;
		} else {
			$col = $col - 1;
		}
		
		if($rarity == 0){ $col = $col - 3;}
		my $S_0 = $table[$col+10]->as_text;
		my $P_0 = $table[$col+11]->as_text;
		my $C_0 = $table[$col+12]->as_text;
		my $S_1 = $table[$col+14]->as_text;
		my $P_1 = $table[$col+15]->as_text;
		my $C_1 = $table[$col+16]->as_text;

		my $newicon = "http://kachagain.com/llsif/buttons/".$id.".png";

		if($#table == $tablesize){
			my @unit_skills = $table[$col+17]->find('b');
			if(defined($unit_skills[0])){
				$unit_skill = $unit_skills[0]->as_text;
    			$unit_skill_detail = $table[$col+17]->as_text;
				$unit_skill_detail =~ s/(?:$unit_skill)//g;
			}else{
				$unit_skill = $table[$col+17]->as_text;
				$unit_skill_detail = '';
			}

			my @center_skills = $table[$col+18]->find('b');
			$center_skill = $center_skills[0]->as_text;
    		$center_skill_detail = $table[$col+18]->as_text;
			$center_skill_detail =~ s/(?:$center_skill)//g;
		}

		my $command = "INSERT INTO center_skill VALUES ('".$center_skill."','".$center_skill_detail."')";
		print $command."\n";
		my $sth = $db->prepare($command);
		$sth->execute;
		$sth->finish;

		$command = "INSERT INTO unit_skill VALUES ('".$unit_skill."','".$unit_skill_detail."')";
		print $command."\n";
		$sth = $db->prepare($command);
		$sth->execute;
		$sth->finish;

		$command = "INSERT INTO carddata VALUES (".$id.",'".$name."','".$series."','".$image_url."','".$imple_info."','".$type."',".$S_0.",".$P_0.",".$C_0.",".$S_1.",".$P_1.",".$C_1.",'".$unit_skill."','".$center_skill."',".$rarity.",".$get_method.",'','','".$newicon."')";
		print $command."\n";
		$sth = $db->prepare($command);
		$sth->execute;
		$sth->finish;

#		print "|".$id."|".$name.":".$series."|".$type."|".$S_0."/".$P_0."/".$C_0."|".$S_1."/".$P_1."/".$C_1."|".$skill."|".$center_skill."|\n"
	}
} 

$db->disconnect;


sub enu{
	return encode('utf-8',$_[0]);
}

