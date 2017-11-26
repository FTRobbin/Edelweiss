import java.util.*;

/**
 * Created by RobbinNi on 26/11/2017.
 */
public interface Environment {

    //Interaction with nodes

    int getN();

    int getCurRound();

    int getID(NaiveVoting p);

    int getInput(NaiveVoting p);

    ArrayList<Message> getInputMessage(NaiveVoting p);

    void putBroadcast(NaiveVoting p, Message m);

    void putOutput(NaiveVoting p, int output);
}
