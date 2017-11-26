import java.util.ArrayList;

/**
 * Created by RobbinNi on 26/11/2017.
 */

public class NaiveVoting {

    public static final int LEADER = 0;

    private final Environment e;

    private int input, output;

    private int[] cnt = new int[2];

    public NaiveVoting(Environment e) {
        this.e = e;
    }

    public void runNode() {
        int round = e.getCurRound();
        if (round == 0) {
            if (e.getID(this) == LEADER) {
                input = e.getInput(this);
                e.putBroadcast(this, new Message(input));
            } else {
                input = -1;
            }
            cnt[0] = cnt[1] = 0;
        } else if (round == 1) {
            ArrayList<Message> msgs = e.getInputMessage(this);
            int b = 0;
            for (Message m : msgs) {
                b = m.getContent();
            }
            e.putBroadcast(this, new Message(b));
        } else if (round == 2) {
            ArrayList<Message> msgs = e.getInputMessage(this);
            for (Message m : msgs) {
                int b = m.getContent();
                if (b == 0 || b == 1) {
                    cnt[b]++;
                }
            }
        } else if (round == 3) {
            System.out.println(e.getID(this) + " : " + cnt[0] + " " + cnt[1]);
            int bar = e.getN() * 2 / 3;
            if (cnt[0] >= bar) {
                output = 0;
            } else if (cnt[1] >= bar) {
                output = 1;
            } else {
                output = -1;
            }
            e.putOutput(this, output);
        } else {
            throw new RuntimeException();
        }
    }
}
