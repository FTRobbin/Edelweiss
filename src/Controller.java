import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * Created by RobbinNi on 26/11/2017.
 */
public class Controller implements Environment {

    private int curRound;

    private Map<NaiveVoting, Integer> nodes;

    private final ExperimentSetting setting;

    private ArrayList<Map.Entry<Integer, Message>> messagePool;

    private ArrayList<ArrayList<Message>> messageBuffer;

    private Map<NaiveVoting, Integer> output;

    public Controller(ExperimentSetting setting) {
        this.setting = setting;
        this.curRound = -1;
        nodes = new HashMap<>();
        messagePool = new ArrayList<>();
        messageBuffer = new ArrayList<>();
        for (int i = 0; i < setting.n; ++i) {
            NaiveVoting node = new NaiveVoting(this);
            nodes.put(node, i);
            messageBuffer.add(new ArrayList<>());
        }
        output = new HashMap<>();
    }

    private boolean isCompleted() {
        return output.size() == setting.n;
    }

    private void nextRound() {
        ++curRound;
        for (Map.Entry<Integer, Message> packet : messagePool) {
            messageBuffer.get(packet.getKey()).add(packet.getValue());
        }
        messagePool.clear();
        for (NaiveVoting node : nodes.keySet()) {
            if (!output.containsKey(node)) {
                node.runNode();
            }
        }
    }

    private void printReport() {
        Set<Map.Entry<NaiveVoting, Integer>> outputSet = output.entrySet();
        for (Map.Entry<NaiveVoting, Integer> it : outputSet) {
            System.out.println(getID(it.getKey()) + " : " + it.getValue());
        }
    }

    // Controller Interface
    public void run() {
        while (!isCompleted()) {
            nextRound();
        }
    }

    public void report() {
        printReport();
    }


    // Environment Interface

    public int getN() {
        return setting.n;
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
            return setting.input;
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
        for (int i = 0; i < setting.n; ++i) {
            messagePool.add(new HashMap.SimpleEntry<>(i, m));
        }
    }

    public void putOutput(NaiveVoting p, int output) {
        if (!nodes.containsKey(p)) {
            throw new RuntimeException();
        }
        this.output.put(p, output);
    }

}
