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

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Properties props = new Properties();
	    props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
	    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
	    String text = "However, their defensive frailties were all too apparent throughout the game and they were hugely indebted to De Gea, who produced no fewer than six excellent saves in a superb performance.";
	    Annotation document = new Annotation(text);
	    
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
	          System.out.print(word+'_'+pos+'_'+ne+' ');
	        }
	        // this is the parse tree of the current sentence
	        Tree tree = sentence.get(TreeAnnotation.class);
	        System.out.print(tree.toString());
	        // this is the Stanford dependency graph of the current sentence
	        SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);
	        System.out.print(dependencies.toList());
	    }
	}

}
