import javafx.util.Pair;

import java.util.*;

/**
 * Created by RobbinNi on 26/11/2017.
 */
public class Environment {

    private final int n;
    private int curRound;

    private int input;

    private Map<NaiveVoting, Integer> nodes;

    private ArrayList<Pair<Integer, Message>> messagePool;

    private ArrayList<ArrayList<Message>> messageBuffer;

    private Map<NaiveVoting, Integer> output;

    public Environment(int n, int leaderInput) {
        this.n = n;
        this.input = leaderInput;
        this.curRound = -1;
        nodes = new HashMap<>();
        messagePool = new ArrayList<>();
        messageBuffer = new ArrayList<>();
        for (int i = 0; i < n; ++i) {
            NaiveVoting node = new NaiveVoting(this);
            nodes.put(node, i);
            messageBuffer.add(new ArrayList<>());
        }
        output = new HashMap<>();
    }

    public boolean isCompleted() {
        return output.size() == n;
    }

    public void nextRound() {
        //TODO: what if a protocol call this
        ++curRound;
        for (Pair<Integer, Message> packet : messagePool) {
            messageBuffer.get(packet.getKey()).add(packet.getValue());
        }
        messagePool.clear();
        for (NaiveVoting node : nodes.keySet()) {
            if (!output.containsKey(node)) {
                node.runNode();
            }
        }
    }

    public void printReport() {
        Set<Map.Entry<NaiveVoting, Integer>> outputSet = output.entrySet();
        for (Map.Entry<NaiveVoting, Integer> it : outputSet) {
            System.out.println(getID(it.getKey()) + " : " + it.getValue());
        }
    }

    public int getN() {
        return n;
    }

    public int getCurRound() {
        return curRound;
    }

    public int getID(NaiveVoting p) {
        if (nodes.containsKey(p)) {
            return nodes.get(p);
        } else {
            throw new RuntimeException();
        }
    }

    public int getInput(NaiveVoting p) {
        int id = getID(p);
        if (id == NaiveVoting.LEADER) {
            return input;
        } else {
            throw new RuntimeException();
        }
    }

    public ArrayList<Message> getInputMessage(NaiveVoting p) {
        int id = getID(p);
        ArrayList<Message> msgs = messageBuffer.get(id);
        messageBuffer.set(id, new ArrayList<>());
        return msgs;
    }

    public void putBroadcast(NaiveVoting p, Message m) {
        if (!nodes.containsKey(p)) {
            throw new RuntimeException();
        }
        for (int i = 0; i < n; ++i) {
            messagePool.add(new Pair<>(i, m));
        }
    }

    public void putOutput(NaiveVoting p, int output) {
        if (!nodes.containsKey(p)) {
            throw new RuntimeException();
        }
        this.output.put(p, output);
    }
}
