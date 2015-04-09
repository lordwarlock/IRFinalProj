import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import java.util.Properties;

import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations.TreeAnnotation;
import edu.stanford.nlp.util.CoreMap;


public class ParseNews {

	public static void parse_line(String line, StanfordCoreNLP pipeline,
								  BufferedWriter pos_writer,
								  BufferedWriter dep_writer,
								  BufferedWriter par_writer) throws IOException{
		
	    Annotation document = new Annotation(line);
	    
	    pipeline.annotate(document);
	    
	    List<CoreMap> sentences = document.get(SentencesAnnotation.class);
	    
	    for(CoreMap sentence: sentences) {
	        // traversing the words in the current sentence
	        // a CoreLabel is a CoreMap with additional token-specific methods
	        for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
	          // this is the text of the token
	          String word = token.get(TextAnnotation.class);
	          // this is the POS tag of the token
	          String pos = token.get(PartOfSpeechAnnotation.class);
	          // this is the NER label of the token
	          String ne = token.get(NamedEntityTagAnnotation.class);     
	          pos_writer.write(word+'_'+pos+'_'+ne+' ');
	        }
	        pos_writer.write('\n');
	        // this is the parse tree of the current sentence
	        Tree tree = sentence.get(TreeAnnotation.class);
	        par_writer.write(tree.toString());
	        par_writer.write('\n');
	        // this is the Stanford dependency graph of the current sentence
	        SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);
	        dep_writer.write(String.join(",",dependencies.toList().split("\n")));
	        dep_writer.write('\n');
	    }
	}
	public static void process_file(File match_file,StanfordCoreNLP pipeline,
			      					String pos_out_dir,
			      					String dep_out_dir,
			      					String par_out_dir) throws IOException{
		BufferedReader reader = new BufferedReader(new FileReader(match_file));
		String name = match_file.getName();
		File pos_out_file = new File(pos_out_dir.concat(name));
		File dep_out_file = new File(dep_out_dir.concat(name));
		File par_out_file = new File(par_out_dir.concat(name));
		BufferedWriter pos_writer = new BufferedWriter(new FileWriter(pos_out_file));
		BufferedWriter dep_writer = new BufferedWriter(new FileWriter(dep_out_file));
		BufferedWriter par_writer = new BufferedWriter(new FileWriter(par_out_file));
		String line;
		try {
			while ((line = reader.readLine()) != null){
				parse_line(line,pipeline,pos_writer,dep_writer,par_writer);
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		pos_writer.close();
		dep_writer.close();
		par_writer.close();
		reader.close();
	}

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		Properties props = new Properties();
	    props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
	    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
	    //String text = "However, their defensive frailties were all too apparent throughout the game and they were hugely indebted to De Gea, who produced no fewer than six excellent saves in a superb performance.";
	    //File match_file = new File("/Users/zheng/Documents/ir/finalproj/data/match/extract/txt_files/E0_01_01_13_Man_City.txt");
	    //process_file(match_file,pipeline);
	    File directory = new File("/Users/zheng/Documents/ir/finalproj/data/match/extract/txt_files/");
	    File[] files_list = directory.listFiles();
	    String pos_out_dir = "/Users/zheng/Documents/ir/finalproj/data/match/extract/pos_files/";
	    String dep_out_dir = "/Users/zheng/Documents/ir/finalproj/data/match/extract/dep_files/";	
	    String par_out_dir = "/Users/zheng/Documents/ir/finalproj/data/match/extract/par_files/";
	    for (int i = 0;i<files_list.length;i++){
	    	if (files_list[i].isFile()){
	    		if (files_list[i].getName().startsWith("E0_")){
	    			System.out.print(files_list[i].getName());
	    			process_file(files_list[i],pipeline,pos_out_dir,dep_out_dir,par_out_dir);
	    		}
	    	}
	    }
	}

}
