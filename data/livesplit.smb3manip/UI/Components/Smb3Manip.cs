namespace LiveSplit.UI.Components
{
    public class Smb3Manip : ISmb3Manip
    {
        private int increment = 1;
        private int initialValue = 0;

        public Smb3Manip(int initialValue = 0, int increment = 1)
        {
            this.initialValue = initialValue;
            this.increment = increment;
            Count = initialValue;
        }

        public int Count { get; private set; }

        public bool Increment()
        {
            if (Count == int.MaxValue)
                return false;

            try
            {
                Count = checked(Count + increment);
            }
            catch (System.OverflowException)
            {
                Count = int.MaxValue;
                return false;
            }

            return true;
        }

        public bool Decrement()
        {
            if (Count == int.MinValue)
                return false;

            try
            {
                Count = checked(Count - increment);
            }
            catch (System.OverflowException)
            {
                Count = int.MinValue;
                return false;
            }

            return true;
        }

        public void Reset()
        {
            Count = initialValue;
        }

        public void SetCount(int value)
        {
            Count = value;
        }

        public void SetIncrement(int incrementValue)
        {
            increment = incrementValue;
        }
    }

    public interface ISmb3Manip
    {
        int Count { get; }

        bool Increment();
        bool Decrement();
        void Reset();
        void SetCount(int value);
        void SetIncrement(int incrementValue);
    }
}