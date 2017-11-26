/**
 * Created by RobbinNi on 26/11/2017.
 */
public class Main {

    static public void main(String[] args) {
        //Get parameters
        int n = 10, leaderInput = 1;
        Environment e = new Environment(n, leaderInput);
        while (!e.isCompleted()) {
            e.nextRound();
        }
        e.printReport();
    }
}
