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

#my $url="https://ラブライブ.gamerch.com/SR_9";
my $url="https://ラブライブ.gamerch.com/SSR_1";
#my $url="https://ラブライブ.gamerch.com/UR_4";

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


# DOM操作してトピックの部分だけ抜き出す。
# <div id='topicsfb'><ul><li>....の部分を抽出する
my $elm  = $tree->look_down('_tag', 'tbody');
my  @list =  $elm->find('tr');
for my $tr (@list) {

	my @table = $tr->find('td');
	if((defined($table[0]) && defined($table[2]))){

		print "table size : ".$#table."\n";

		my $col = 0;

    	my $id = $table[$col]->as_text;

		my $fullimg_0="";
		my $fullimg_1="";

		my @image_tag = $table[$col+2]->find('a');
		if(@image_tag!=0){
			$fullimg_0 = $image_tag[0]->attr('href');
		}
		@image_tag = $table[$col+3]->find('a');
		if(@image_tag!=0){
			$fullimg_1 = $image_tag[0]->attr('href');
		}


		my $command = "UPDATE carddata SET fullimg_0='".$fullimg_0."',fullimg_1='".$fullimg_1."' where id=".$id;
		print $command."\n";
		my $sth = $db->prepare($command);
		$sth->execute;
		$sth->finish;

	}
} 

$db->disconnect;


sub enu{
	return encode('utf-8',$_[0]);
}

